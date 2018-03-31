from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()
alerts_needing_update = Alert.find_needing_update()
for alerts in alerts_needing_update:
    alerts.load_item_price()
    alerts.send_message_when_reached()