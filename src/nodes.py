

from indy import pool, wallet, did, ledger, anoncreds, blob_storage

async def run:

    logger.info("==============================")
    logger.info("=== Getting Trust Anchor credentials for Uniandes, Entry and Sicua  ==")
    logger.info("------------------------------")

    steward = {
        'name': "Sovrin Steward",
        'wallet_config': json.dumps({'id': 'sovrin_steward_wallet'}),
        'wallet_credentials': json.dumps({'key': 'steward_wallet_key'}),
        'pool': pool_['handle'],
        'seed': '000000000000000000000000Steward1'
    }
    await create_wallet(steward)
    logger.info("\"Sovrin Steward\" -> Create and store in Wallet DID from seed")
    steward['did_info'] = json.dumps({'seed': steward['seed']})
    steward['did'], steward['key'] = await did.create_and_store_my_did(steward['wallet'], steward['did_info'])

    logger.info("==============================")
    logger.info("== Getting Trust Anchor credentials - Uniandes getting Verinym  ==")
    logger.info("------------------------------")
     
    uniandes = {
        'name': 'Uniandes',
        'wallet_config': json.dumps({'id': 'uniandes_wallet'}),
        'wallet_credentials': json.dumps({'key': 'uniandes_wallet_key'}),
        'pool': pool_['handle'],
        'role': 'TRUST_ANCHOR'
    }

    await getting_verinym(steward, uniandes)

    logger.info("==============================")
    logger.info("== Getting Trust Anchor credentials - Entry getting Verinym  ==")
    logger.info("------------------------------")

    entry = {
        'name': 'Entry',
        'wallet_config': json.dumps({'id': 'entry_wallet'}),
        'wallet_credentials': json.dumps({'key': 'entry_wallet_key'}),
        'pool': pool_['handle'],
        'role': 'TRUST_ANCHOR'
    }

    await getting_verinym(steward, entry)

    logger.info("==============================")
    logger.info("== Getting Trust Anchor credentials - Sicua getting Verinym  ==")
    logger.info("------------------------------")

    sicua = {
        'name': 'Sicua',
        'wallet_config': json.dumps({'id': 'sicua_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sicua_wallet_key'}),
        'pool': pool_['handle'],
        'role': 'TRUST_ANCHOR'
    }

    await getting_verinym(steward, sicua)

    logger.info("------------------------------")
    logger.info("== Student/User setup ==")
    logger.info("------------------------------")

    susan = {
        'name': 'Susan',
        'wallet_config': json.dumps({'id': 'susan_wallet'}),
        'wallet_credentials': json.dumps({'key': 'susan_wallet_key'}),
        'pool': pool_['handle'],
    }

    name = input("Name:")
    user =  {}
    user['first_name'] = name
    last_name = input("Last Name:")
    user['last_name']=last_name
    print("Type of user: ")
    print("1. Student ")
    print("2. Teacher ")
    print("3. Employee")
    print("4. Invited")
    type_of_user = int(input("Enter the number for your type of user: "))
    if type_of_user == 1:
        status='student'
    elif type_of_user == 2:
        status = 'teacher'
    elif type_of_user == 3:
        status = 'Employee'
    elif type_of_user == 4:
        status = 'Invited'
    else: 
        print("Enter a valid number")           
    user['status']=status
    id = input("ID:")
    user['id'] = id
    print("First name: " + user['first_name'])
    print("Last name: " + user['last_name'])
    print("User: "+ user['status'])
    print("ID: "+ user['id'])


    await create_wallet(susan)
    (susan['did'], susan['key']) = await did.create_and_store_my_did(susan['wallet'], "{}")

    async def create_wallet(identity):
    logger.info("\"{}\" -> Create wallet".format(identity['name']))
    try:
        await wallet.create_wallet(wallet_config("create", identity['wallet_config']),
                                   wallet_credentials("create", identity['wallet_credentials']))
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
            pass
    identity['wallet'] = await wallet.open_wallet(wallet_config("open", identity['wallet_config']),
                                                  wallet_credentials("open", identity['wallet_credentials']))
def wallet_config(operation, wallet_config_str):
    if not args.storage_type:
        return wallet_config_str
    wallet_config_json = json.loads(wallet_config_str)
    wallet_config_json['storage_type'] = args.storage_type
    if args.config:
        wallet_config_json['storage_config'] = json.loads(args.config)
    # print(operation, json.dumps(wallet_config_json))
    return json.dumps(wallet_config_json)


def wallet_credentials(operation, wallet_credentials_str):
    if not args.storage_type:
        return wallet_credentials_str
    wallet_credentials_json = json.loads(wallet_credentials_str)
    if args.creds:
        wallet_credentials_json['storage_credentials'] = json.loads(args.creds)
    # print(operation, json.dumps(wallet_credentials_json))
    return json.dumps(wallet_credentials_json)

async def getting_verinym(from_, to):
    await create_wallet(to)

    (to['did'], to['key']) = await did.create_and_store_my_did(to['wallet'], "{}")

    from_['info'] = {
        'did': to['did'],
        'verkey': to['key'],
        'role': to['role'] or None
    }

    await send_nym(from_['pool'], from_['wallet'], from_['did'], from_['info']['did'],
                   from_['info']['verkey'], from_['info']['role'])

async def send_nym(pool_handle, wallet_handle, _did, new_did, new_key, role):
    nym_request = await ledger.build_nym_request(_did, new_did, new_key, None, role)
    await ledger.sign_and_submit_request(pool_handle, wallet_handle, _did, nym_request)