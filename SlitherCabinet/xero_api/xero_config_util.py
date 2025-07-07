import yaml

#get value from config file
def get_yaml_value(*keys):
    file_path='C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/xero_api/xero_config.yaml'
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    # Navigate nested keys
    value = config
    for key in keys:
        value = value.get(key)
        if value is None:
            return None

    return value

#update Refresh Token in config File
def update_config(key, new_value):
    file_path='C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/xero_api/xero_config.yaml'
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)

    config[key] = new_value

    with open(file_path, 'w') as f:
        yaml.dump(config, f, width=400)
    print(f"Updated {key} to {new_value}")



