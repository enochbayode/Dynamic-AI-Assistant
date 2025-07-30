import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=OPENAI_API_KEY)

# Fallback intent
FALLBACK_INTENT = "unknown"

# Few-shot examples to improve classification accuracy
FEW_SHOT_LEARNING = [
    {"role": "user", "content": "hello, hey or hey there, I need help"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "Enlighten me about the services you provided on this platform."},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "How can I make payment?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "What does your platform do?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "Can you tell me about your services?"},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "I want to delete my account."},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "What is the refund policy?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "I want to update my profile, how can do that?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "Does this platform supports HIPAA compliance?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "How do I book a session?"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "Take me to the admin dashboard, please."},
    {"role": "assistant", "content": "Intent: dashboard_access"},

    {"role": "user", "content": "Go to the admin home page, I want to see my profile."},
    {"role": "assistant", "content": "Intent: dashboard_access"},

    {"role": "user", "content": "I want to return to the admin home screen."},
    {"role": "assistant", "content": "Intent: dashboard_access"},    

    {"role": "user", "content": "Show me the reports section."},
    {"role": "assistant", "content": "Intent: dashboard_access"},

    {"role": "user", "content": "Open analytics — I want to see the insights."},
    {"role": "assistant", "content": "Intent: dashboard_access"},

    {"role": "user", "content": "I want to add a new credit card for my payments."},
    {"role": "assistant", "content": "Intent: client_dashboard"},

    {"role": "user", "content": "Take me to the home page, I want to see my profile."},
    {"role": "assistant", "content": "Intent: client_dashboard"},

    {"role": "user", "content": "How do I update my current payment method?"},
    {"role": "assistant", "content": "Intent: client_dashboard"},

    {"role": "user", "content": "I’d like to link my bank account for direct payments."},
    {"role": "assistant", "content": "Intent: client_dashboard"},
    
    {"role": "user", "content": "Can you help me enable automatic payments?"},
    {"role": "assistant", "content": "Intent: client_dashboard"},

    {"role": "user", "content": "I need to remove my expired credit card from the platform."},
    {"role": "assistant", "content": "Intent: client_dashboard"},

    {"role": "user", "content": "I want to book a session with a therapist."},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "I want to schedule an appointment."},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "I want to schedule a session."},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "I want to book a session"},
    {"role": "assistant", "content": "Intent: info_query"},

    {"role": "user", "content": "Can I see available therapists?"},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "what are the services you available?"},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "Tell me about your services on this platform."},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "How do I find a service?"},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "List all the mental health services I can access."},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "What kind of services are available?"},
    {"role": "assistant", "content": "Intent: service_search"},
    
    {"role": "user", "content": "Show me the assessments I can book."},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "I’d like to search for speech therapy options."},
    {"role": "assistant", "content": "Intent: service_search"},
    
    {"role": "user", "content": "Can you help me find therapy services?"},
    {"role": "assistant", "content": "Intent: service_search"},

    {"role": "user", "content": "Can you show me the list of therapists registered under our organization?"},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I need to check which team members are currently assigned to speech therapy services."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Who are the active clinicians on our team this month?"},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Find all professionals tagged under behavioural assessments for our organization."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Show me all registered staff members and let me manage their access. "},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I want to update the details of one of our staff members."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I'd like to deactivate this staff member—they’re no longer active for now"},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I want to permanently delete this staff member from my records."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I'd like to edit the details of a provider, including the contact info."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Remove this provider completely from our system."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I'd like to activate a provider who was previously inactive."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Show me all clinicians so I can manage their profiles."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I need to edit the profile of a clinician to reflect their new role."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I want to delete a clinician from our organization’s database."},
    {"role": "assistant", "content": "Intent: team_member_search"},
    
    {"role": "user", "content": "I will like to reactivate a clinician's account so they can log in again."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I want to manage team members in our organization."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I would like to update a team member’s information."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Delete a team member from the team schedule."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Help me activate a deactivated team member"},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "I want to add someone to the team"},
    {"role": "assistant", "content": "Intent: create_team_member"},

    {"role": "user", "content": "How do I create a new staff profile"},
    {"role": "assistant", "content": "Intent: create_team_member"},

    {"role": "user", "content": "Where do I go to onboard a provider?"},
    {"role": "assistant", "content": "Intent: create_team_member"},

    {"role": "user", "content": "Take me to the page to register a new clinician"},
    {"role": "assistant", "content": "Intent: create_team_member"},

    {"role": "user", "content": "I want to add a new patient"},
    {"role": "assistant", "content": "Intent: create_patient"},

    {"role": "user", "content": "How do I create a new patient profile"},
    {"role": "assistant", "content": "Intent: create_patient"},

    {"role": "user", "content": "Where do I go to onboard a new client?"},
    {"role": "assistant", "content": "Intent: create_patient"},

    {"role": "user", "content": "I want to add a new client"},
    {"role": "assistant", "content": "Intent: create_patient"},

    {"role": "user", "content": "I need to search for a patient"},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "How do I see my patients?"},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "I want to see my patients"},
    {"role": "assistant", "content": "Intent: search_patient"},
 
    {"role": "user", "content": "Show me all patients so I can manage their records."},
    {"role": "assistant", "content": "Intent: search_patient"},
    
    {"role": "user", "content": "I need to update a patient’s details."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Please deactivate this patient’s account temporarily."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "navigate me to the patient page, I want to see all my patients"},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "I want to see all my clients"},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Reactivate this patient’s profile for access again."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Deactivate this client—they’re no longer active."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Help me manage all existing clients in the system."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Edit this client’s information—it needs to be updated."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Delete this client’s record from the database."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Activate this client’s profile so they can use the service again."},
    {"role": "assistant", "content": "Intent: search_patient"},

    {"role": "user", "content": "Show me the appointments I have"},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "I’d like to create a new appointment for a patient."},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "Show me all upcoming appointments so I can manage them."},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "I want to see my appointments"},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "Can you help me schedule an appointment for tomorrow?"},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "How do I find my appointments "},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "Please reschedule this appointment to next Monday."},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "Cancel the appointment set for 3 PM today for me."},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "How many appointments do I have this week?"},
    {"role": "assistant", "content": "Intent: appointment_search"},

    {"role": "user", "content": "I’d like to book an appointment."},
    {"role": "assistant", "content": "Intent: client_appointment"},

    {"role": "user", "content": "Can I schedule a session with my therapist?"},
    {"role": "assistant", "content": "Intent: client_appointment"},

    {"role": "user", "content": "Show me available time slots for a session."},
    {"role": "assistant", "content": "Intent: client_appointment"},

    {"role": "user", "content": "I want to reserve a time with my therapist."},
    {"role": "assistant", "content": "Intent: client_appointment"},
    
    {"role": "user", "content": "I need to see someone soon, can you help me schedule?"},
    {"role": "assistant", "content": "Intent: client_appointment"},
    
    {"role": "user", "content": "Can you help me find a clinic?"},
    {"role": "assistant", "content": "Intent: client_practice_search"},

    {"role": "user", "content": "Show me the providers I can choose from."},
    {"role": "assistant", "content": "Intent: client_practice_search"},

    {"role": "user", "content": "Can you look up a specific practice location for me?"},
    {"role": "assistant", "content": "Intent: client_practice_search"},

    {"role": "user", "content": "Use the clinic finder to search for a facility."},
    {"role": "assistant", "content": "Intent: client_practice_search"},

    {"role": "user", "content": "Let me view and manage the current provider schedules."},
    {"role": "assistant", "content": "Intent: team_member_search"},

    {"role": "user", "content": "Take me to the practice locations page."},
    {"role": "assistant", "content": "Intent: practice_locations"},
    
    {"role": "user", "content": "I want to manage our clinic locations."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "Help me edit one of our practice locations."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "Add a new branch to our locations."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "Remove one of the listed clinic locations."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "I need to update our clinic’s address."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "Set up a new office branch."},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "Where are all our offices listed?"},
    {"role": "assistant", "content": "Intent: practice_locations"},

    {"role": "user", "content": "I want to manage all saved contacts."},
    {"role": "assistant", "content": "Intent: contact_page"},

    {"role": "user", "content": "Can I add a new emergency contact?"},
    {"role": "assistant", "content": "Intent: contact_page"},

    {"role": "user", "content": "I need to update some contact details."},
    {"role": "assistant", "content": "Intent: contact_page"},

    {"role": "user", "content": "Please help me delete a contact from the list."},
    {"role": "assistant", "content": "Intent: contact_page"},

    {"role": "user", "content": "How do I update the referral source for a patient?"},
    {"role": "assistant", "content": "Intent: contact_page"},
    
    {"role": "user", "content": "Show me the full contact list, please."},
    {"role": "assistant", "content": "Intent: contact_page"},

    {"role": "user", "content": "I want to manage all payer accounts."},
    {"role": "assistant", "content": "Intent: payer_page"},
    
    {"role": "user", "content": "I'd like to add a new insurance company to our system?"},
    {"role": "assistant", "content": "Intent: payer_page"},

    {"role": "user", "content": "Please help me remove a payer from the list."},
    {"role": "assistant", "content": "Intent: payer_page"},

    {"role": "user", "content": "I need to update the information of a payer."},
    {"role": "assistant", "content": "Intent: payer_page"},

    {"role": "user", "content": "I'd like to edit the insurance company details?"},
    {"role": "assistant", "content": "Intent: payer_page"},
    
    {"role": "user", "content": "Show me a list of all registered payers." },
    {"role": "assistant", "content": "Intent: payer_page"},
    
    {"role": "user", "content": "I want to manage our billing accounts."},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content":  "Show me all the invoices we've issued."},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content": "Can I generate a new invoice for a patient?"},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content": "Help me edit a billing entry."},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content": "I’d like to review our billing history."},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content": "Please show outstanding or unpaid bills."},
    {"role": "assistant", "content": "Intent: billing_page"},

    {"role": "user", "content": "I want to manage patient prescriptions."},
    {"role": "assistant", "content": "Intent: e-prescriptions"},

    {"role": "user", "content": "Help me create a new e-prescription."},
    {"role": "assistant", "content": "Intent: e-prescriptions"},

    {"role": "user", "content": "I need to edit a prescription I issued earlier."},
    {"role": "assistant", "content": "Intent: e-prescriptions"},

    {"role": "user", "content": "Can I process a medication refill for a patient?"},
    {"role": "assistant", "content": "Intent: e-prescriptions"},

    {"role": "user", "content": "Show me the patient's medication history."},
    {"role": "assistant", "content": 'Intent: e-prescriptions'},

    {"role": "user", "content": "I’d like to cancel an existing prescription."},
    {"role": "assistant", "content": 'Intent: e-prescriptions'},

    {"role": "user", "content": "I want to manage all uploaded files as an admin."},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "As an admin, I'd like to upload a new file to the system?"},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "Show me all shared documents, as an admin."},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "Where can I view files linked to a patient?"},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "As an admin, I need to update the details of a file."},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "As an admin, I'd like to delete an old file from the system."},
    {"role": "assistant", "content": "Intent: manage_file"},

    {"role": "user", "content": "I’d like to set up the payment gateway."},
    {"role": "assistant", "content": "Intent: manage_payment"},

    {"role": "user", "content": "Where do I update our Stripe integration details?"},
    {"role": "assistant", "content": 'Intent: manage_payment'},

    {"role": "user", "content": "Show me where I can manage available payment methods."},
    {"role": "assistant", 'content': 'Intent: manage_payment'},

    {"role": "user", "content": "How do I change the default payment processor?"},
    {"role": "assistant", "content": "Intent: manage_payment"},

    {"role": "user", "content": "I need to update our practice information."},
    {"role": 'assistant', 'content': 'Intent: manage_practice'},

    {"role": "user", "content": "Where can I change the clinic’s name?"},
    {"role": "assistant", "content": "Intent: manage_practice"},

    {"role": 'user', 'content': "Help me update the clinic operating hours."},
    {"role": 'assistant', 'content': 'Intent: manage_practice'},

    {"role": "user", "content": "How do I update the list of specialties we offer?"},  
    {"role": 'assistant', 'content': 'Intent: manage_practice'},

    {"role": 'user', 'content': "I’d like to update our billing preferences."},
    {"role": 'assistant', 'content': 'Intent: billing_settings'},

    {"role": 'user', 'content': "I'd like to customize the invoice template?"},
    {"role": 'assistant', 'content': 'Intent: billing_settings'},

    {"role": 'user', 'content': "Where do I add our clinic’s tax details?"},
    {"role": 'assistant', 'content': 'Intent: billing_settings'},

    {"role": "user", "content": "Help me enable late payment fees for overdue invoices."},
    {"role": 'assistant', 'content': 'Intent: billing_settings'},

    {"role": 'user', 'content': "As an admin, I need to manage the admins permissions of my organization."},
    {"role": 'assistant', 'content': 'Intent: admin_settings'},

    {"role": 'user', 'content':  "As an admin, how do I change my password?"},
    {"role":  'assistant',  'content':  'Intent: admin_settings'},

    {"role": "user", "content": "I'd like to assign a new admin to the platform."},
    {"role": 'assistant', 'content': 'Intent: admin_settings'},

    {"role": "user", "content": "show me the admin settings."},
    {"role": 'assistant', 'content': 'Intent: admin_settings'},

    {"role": "user", "content": "I want to upload my documents."},
    {"role": 'assistant', 'content': 'Intent: client_document'},

    {"role": "user", "content": "Where can I view the forms shared with me?"},
    {"role": 'assistant', 'content': 'Intent: client_document'},
    
    {"role": "user", "content": "I need to download my consent form."},
    {"role": 'assistant', 'content': 'Intent: client_document'},

    {"role": "user", "content": "How do I submit my insurance card?"},
    {"role": 'assistant', 'content': 'Intent: client_document'},

    {"role": "user", "content": "Show me my treatment plan documents."},
    {"role": 'assistant', 'content': 'Intent: client_document'},

]

async def classify_intent(
    user_query: str,
    user_id: str,
    assistant_session_id: str,
    organization_id: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.5, # lower temperature increase accuracy for this task
) -> str:
    """
    Classifies the user's intent using OpenAI API with few-shot examples.

    Returns an intent string like: service_search, info_query, team_member_search, 'create_team_member', 'search_appointment', or unknown.
    """

    try:
        messages = FEW_SHOT_LEARNING + [
            {"role": "user", "content": f"{user_query}"},
        ]

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": """
                        You are an intent classifier for a multi-tenant AI assistant.

                        Given a user's query, classify the intent into one of the following categories:

                        - `info_query`: The user is asking a general question, greeting, or informational request not tied to service discovery (e.g., "Hello", "How does this work?", "Tell me about the platform", "Where is my profile?").
                        - `dashboard_access`: The user who is an Admin is looking to access or navigate the dashboard or home page (e.g., "Take me to the admin dashboard", "Go to the admin home page", "Show me the reports section").
                        - `service_search`: The user is looking for services or making a request related to services (e.g., "Book a speech therapist", "Show me therapy services", "Find counseling support").
                        - `team_member_search`: The user is looking for information about team members or clinicians (e.g., "Who are the therapists in our organization?", "List all team members", "Find all professionals tagged under behavioural assessments for our organization.").
                        - `create_team_member`: The user is looking to create or add a new team member (e.g., "I want to add someone to the team", "How do I create a new staff profile", "Where do I go to onboard a provider?").
                        - `create_patient`: The user is looking to create or add a new patient (e.g., "I want to add a new patient", "How do I create a new patient profile", "Where do I go to onboard a new client?").
                        - `search_patient`: The user is looking to search or view their patients (e.g., "I want to search for a patient", "How do I see my patients?", "I want to see all my patients").
                        - `appointment_search`: The user is looking to search or view their appointments (e.g., "I want to see my appointments", "Show me the appointments I have", "Find all my appointments").
                        - `client_appointment`: The user is looking to book or manage their own appointments (e.g., "I want to book a session", "Can I schedule a session with my therapist?", "Show me available time slots for a session").
                        - `practice_locations`: The user is looking to manage or view practice locations (e.g., "Take me to the practice locations page", "I want to manage our clinic locations", "Help me edit one of our practice locations").
                        - `billing_page`: The user is looking to manage or view billing information (e.g., "I want to manage our billing accounts", "Show me all the invoices we've issued", "Can I generate a new invoice for a patient?").
                        - `payer_page`: The user is looking to manage or view payer information (e.g., "I want to manage all payer accounts", "I'd like to add a new insurance company to our system?", "Please help me remove a payer from the list.").
                        - `contact_page`: The user is looking to manage or view contact information (e.g., "I want to manage all saved contacts", "Can I add a new emergency contact?", "I need to update some contact details.").
                        - `e-prescriptions`: The user is looking to manage or view e-prescriptions (e.g., "I want to manage patient prescriptions", "Help me create a new e-prescription", "I need to edit a prescription I issued earlier").
                        - `manage_file`: The user who is an asmin is looking to manage files or documents (e.g., "I’d like to upload a document to the system as an admin", "As an admin, how can I delete a file from the system?", "Show me the list of documents I’ve uploaded as an admin.").
                        - `manage_payment`: The user is looking to manage payment methods or transactions (e.g., "I want to add a new payment method", "How do I view my payment history", "Show me my payment methods").
                        - `manage_practice`: The user is looking to manage practice settings or configurations (e.g., "I want to update my practice settings", "How do I change my practice information", "Show me my practice details").
                        - `billing_settings`: The user is looking to manage billing settings (e.g., "I want to update my billing settings", "How do I change my billing information", "Show me my billing preferences").
                        - `admin_settings`: The user is looking to manage admin settings or permissions (e.g., "I want to add a new admin to my organization", "How do I manage admin permissions", "Show me the admin settings").
                        - `client_dashboard`: The user is looking to manage their client dashboard or profile (e.g., "I want to update my profile", "How do I update my current payment method?", "Take me to the home page").
                        - `client_document`: The user is looking to manage or view their documents (e.g., "I want to upload my documents", "Where can I view the forms shared with me?", "I need to download my consent form").
                        - `client_practice_search`: The user is looking to search for clinics or providers (e.g., "Can you help me find a clinic?", "Show me the providers I can choose from", "Can you look up a specific practice location for me?").
                        
                        Rules:
                        - Always return one of: `service_search`, `team_member_search`, `create_team_member`, `create_patient`, `search_patient`,  
                          `dashboard_access`, `page_locations`, `appointment_search`, `billing_page`, `payer_page`, `contact_page`, `e-prescriptions`, `manage_file`, `manage_payment`, `manage_practice`,
                          `billing_settings`, `admin_settings`, `client_dashboard`, `client_document`, `client_practice_search` or `info_query`

                        - If the query is a greeting or conversational like "hi", "how are you?", classify it as `info_query`.
                        - Do not explain or justify the classification, just return the label.

                        Examples:
                        User: "I want to see available therapy services"
                        Intent: service_search

                        User: "Hey, how’s it going?"
                        Intent: info_query

                        User: "What's the weather in London?"
                        Intent: unknown

                        User: "Can I book a physiotherapy session?"
                        Intent: service_search

                        User: "How do I update my settings?"
                        Intent: info_query

                        User: "Show me the team members in our organization"
                        Intent: team_member_search

                        User: "I want to add a new clinician to our team"
                        Intent: create_team_member

                        User: "I want to add a new client"
                        Intent: create_patient

                        User: "I want to see all my patients"
                        Intent: search_patient

                        User: "Show me the appointments I have on my calender ?"
                        Intent: appointment_search

                        User: "I want to book a session with my therapist"
                        Intent: client_appointment

                        User: "Take me to the admin dashboard, I want to see my reports"
                        Intent: dashboard_access

                        User: "Where are all our offices listed?"
                        Intent: practice_locations

                        User: "I want to manage our billing accounts."
                        Intent: billing_page

                        User: "I want to manage all payer accounts."
                        Intent: payer_page

                        User: "I want to manage all saved contacts."
                        Intent: contact_page

                        User: "I want to manage patient prescriptions."
                        Intent: e-prescriptions

                        User: "I want to upload a document as an admin."
                        Intent: manage_file

                        User: "I want to add a new payment method."
                        Intent: manage_payment

                        User: "I want to update my practice settings."
                        Intent: manage_practice

                        User: "I want to update my billing settings."
                        Intent: billing_settings

                        User: "I want to add a new admin to my organization."
                        Intent: admin_settings

                        User: "I want to update my profile."
                        Intent: client_dashboard

                        User: "I want to upload my documents."
                        Intent: client_document

                        User: "Can you help me find a clinic?"
                        Intent: client_practice_search
                    """
                },

                *messages
            ],
            temperature=temperature,
            max_tokens=30,
        )

        intent_raw = response.choices[0].message.content.strip()
        intent = intent_raw.lower().replace("intent:", "").strip()

        if intent not in {
            "info_query",
            "service_search",  
            "team_member_search", 
            "create_team_member", 
            "create_patient", 
            "search_patient",
            "appointment_search",
            "dashboard_access",
            "practice_locations",
            "contact_page",
            "payer_page",
            "billing_page",
            "e-prescriptions",
            "manage_file",
            "manage_payment",
            "manage_practice",
            "billing_settings",
            "admin_settings",
            "client_dashboard",
            "client_appointment",
            "client_practice_search",
            "client_document"  

        }:
        
            intent = FALLBACK_INTENT

        return intent

    except Exception as e:
        print(f"Intent classification failed: {e}")
        return FALLBACK_INTENT
