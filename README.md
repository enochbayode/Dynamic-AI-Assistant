# Documentation
# Install library dependencies

pip install -r requirements.txt

run this app with

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Then, open http://127.0.0.1:8000 in your browser to see the welcome message.

The swagger for all the endpoints are available here: http://127.0.0.1:8000/docs






| Channel             | Behavior                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| **Assistant**       | Shows a quick summary of top 5 relevant services (from page 1 only).                             |
| **Frontend Widget** | Receives `services`, shows them, and lets the user paginate via the platform’s UI.         |
| **Link**            | Assistant includes a `view_all_url` so the user can jump into the full service listing manually. |


In Guzape, we have the SmartVista Estate, which features fully automated 4-bed duplexes priced at ₦350 million. It includes a Certificate of Occupancy (C of O), solar backup, CCTV, smart locks, and amenities like a gym and pool. The estate is completed and ideal for high-net-worth individuals and diaspora families. Would you like to schedule an inspection or learn more about it?