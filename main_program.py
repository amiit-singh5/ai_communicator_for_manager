from tools.logger_setup import setup_logger
from tools.config_reader import ConfigurationReader
from tools.session_manager import SessionManager

logger = setup_logger()

logger.info("Calling from main program...")
print("Calling from main program...")
logger.info(ConfigurationReader().get_logging_config())
logger.info(ConfigurationReader().get_openroute_config())

url = ConfigurationReader().get_url()
headers = ConfigurationReader().get_headers()
message = ConfigurationReader().get_json_message()
print("url : ", url)
print("headers : ",headers)
print("message : ", message)

with SessionManager() as session:
    session.configure(base_url=url, headers=headers, json_message=message)
    response = session.post("") #, data=headers, json=message)
    print("Status Code:", response.status_code)
    logger.info(f"Response JSON:, {response.json()}")
    print("Raw Text:", response.text)
    try:
        reply = response.json()['choices'][0]['message']['content']
        print("\nAssistant's Reply:\n", reply)
        logger.info(f"Assistant Reply: {reply}")
    except Exception as e:
        logger.error(f"Error extracting assistant response: {e}")