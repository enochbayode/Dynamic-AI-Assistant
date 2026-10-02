import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


async def openai_generate_response_summary(
        system_prompt: str, 
        user_prompt: str, 
        model: str = "gpt-4o-mini", 
        temperature: float = 0.5, 
        max_tokens: int = 300
    ) -> str:

    """
    Generic function to generate responses using OpenAI's chat API.

    :param system_prompt: Instruction to guide the assistant's behavior.
    :param user_query: Content or query from the user.
    :param model: OpenAI model name.
    :param temperature: Sampling temperature (creativity level).
    :param max_tokens: Max tokens in the response.
    :return: AI-generated response.
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, but I couldn't process your request."

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred."
    

# >>>>>>>>>>>>>>>>>>>> Task functions for Admins >>>>>>>>>>>>>>>>>>>>>>>>>> 

async def dashboard_generate_response_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly and concise message guiding the Admin to the dashboard based on their query.

    :param user_query: Admin's input related to accessing the dashboard.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: AI-generated summary message for navigating to the dashboard.
    """

    user_prompt = (
        f"The following is a request from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Write a clear and concise message guiding the Admin to the admin dashboard. "
        "Assume the Admin is asking to view reports, metrics, or return to the home screen. "
        "Use a supportive and friendly tone. "
        "Let them know that a link will be provided to access the dashboard directly."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant on  telehealth platform for healthcare professionals.
            Your role is to assist Admins in navigating to the dashboard.
            Based on their query, provide a short, friendly message guiding them to the main dashboard.
            Clearly confirm their intent and inform them that a link will be available for quick access to the dashboard.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_service_summary(
    services: list,
    user_query: str, # raw input from user 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Creates a friendly summary of services based on user query.

    :param services: List of services with name, description, and url.
    :param user_query: User's service-related input.
    :param user_id: ID of the client (for tracking or personalization).
    :param session_id: Session ID for conversation tracking.
    :param organization_id: Organization to support multi-tenancy.
    :return: AI-generated summary.
    """

    context = "\n\n".join([
        f"Service: {s['name']}\nDescription: {s['description']}\nAmount: {s['amount']}"
        for s in services
    ])

    user_prompt = (
        f"User ID: {user_id}, Session ID: {assistant_session_id}, Organization: {organization_id}\n"
        f"The user asked: '{user_query}'\n\n"
        f"Based on the following services, write a concise and helpful sentence like an AI assistant:\n\n{context}\n\n"
        "Each service should be briefly described. Use a friendly and informative tone."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant that summarizes services for users on a telehealth platform, 
            a telehealth platform for healthcare professionals.
            Your task is to provide a friendly and informative write up of the services based on user query.
            Ensure your response is tailored to the user's query and context.
            After which you will ask the user to continue the booking on the main screen.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.5,
        max_tokens=300
    )

async def generate_team_member_summary(
    team_members: list,
    user_query: str, # raw input from user 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Creates a friendly summary of team members based on user query.

    :param team_members: List of team members with name, description, and url.
    :param user_query: User's service-related input.
    :param user_id: ID of the client (for tracking or personalization).
    :param session_id: Session ID for conversation tracking.
    :param organization_id: Organization to support multi-tenancy.
    :return: AI-generated summary.
    """

    context = "\n\n".join([
        f"Team Member: {tm['title']}, {tm['name']}\nPrimary language: {tm['primary_language']}\nTime zone: {tm['time_zone']}"
        for tm in team_members
    ])

    user_prompt = (
        f"User ID: {user_id}, Session ID: {assistant_session_id}, Organization: {organization_id}\n"
        f"The user asked: '{user_query}'\n\n"
        f"Based on the {user_query} and following team members, write a concise and helpful text like an AI assistant:\n\n{context}\n\n"
        "Each team member should be briefly described. Use a friendly and informative tone."
    )

    
    return  await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant that summarizes team members for users on 
            a telehealth platform for healthcare professionals.
            Your task is to provide a friendly and informative write up of the team members/staffs based on user query.
            After which you will ask the user to see more details on the main screen.
            Ensure your response is tailored to the user's query and context.
            You can also ask the user to use the link below to navigates to the team members page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.5,
        max_tokens=300
    )

async def generate_create_team_member_summary(
    user_query: str,
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Creates a friendly summary of creating a team member based on user query.

    :param user_query: User's service-related input.
    :param user_id: ID of the client (for tracking or personalization).
    :param session_id: Session ID for conversation tracking.
    :param organization_id: Organization to support multi-tenancy.
    :return: AI-generated summary.
    """

    user_prompt = (
        f"User ID: {user_id}, Session ID: {assistant_session_id}, Organization: {organization_id}\n"
        f"The user asked: '{user_query}'\n\n"
        f"Write a concise and helpful sentence like an AI assistant about creating a new team member based on {user_query}."
        "In this case you're referring to an Admin hence treat them as one, use a friendly and informative tone."
        "You can also ask the admin to use the link below to navigates to the staff creation page"
    )

    
    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant that provides information on creating team members for Admins on 
            a telehealth platform for healthcare professionals.
            Your task is to provide a friendly guidiance on creating a new team member based on user query
            After which you can ask the Admin to see more details on the main screen or use the link below.
            Ensure your response is tailored to the user's query and context.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_create_patient_summary(
    user_query: str,
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a concise and friendly message guiding the Admin on how to create a new patient based on their query.

    :param user_query: Admin's input related to patient creation.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: AI-generated summary message for patient creation.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Generate a helpful, concise, and friendly message guiding the admin on how to create a new patient. "
        "Assume the Admin wants to register a new patient in the system. "
        "Keep the tone professional and supportive. "
        "Mention that a link will be provided to access the patient creation page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant on a telehealth platform for healthcare professionals.
            Your role is to guide Admin users when they want to create or register a new patient.
            Respond to the query with a short, friendly, and informative sentence that confirms their intent 
            and directs them to the appropriate action.
            Let the Admin know that a link will be provided to navigate to the patient creation page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_patient_search_summary(
    user_query: str,  
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a concise and friendly message to guide the Admin to the Patient page based on their query.

    :param user_query: Admin's input related to patient search or management.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: AI-generated navigation message for the patient page.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Generate a short and helpful message guiding the admin to the Patient page. "
        "Assume they want to view, manage, edit, activate, or deactivate patient records. "
        "Your tone should be friendly and professional, like an AI assistant helping them navigate the system. "
        "Mention that a link will be provided to access the Patient management section."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful assistant on a telehealth platform for healthcare professionals.
            When an admin makes a request related to patients—such as viewing, editing, activating, or deactivating—
            respond with a concise and friendly message directing them to the Patient page.
            Let the admin know they can manage all patient-related tasks there.
            Conclude by informing them that a link will be provided to navigate to the Patient management page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_search_appointment_summary(
    user_query: str,  # raw input from user 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a helpful navigation message in response to a user query related to appointments.

    :param user_query: User's input related to appointments.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Generate a short, friendly response guiding the admin to the Appointments page. "
        "Assume they are trying to view, search, manage, reschedule, or cancel appointments. "
        "Write your response as an AI assistant and let the admin know they can perform all appointment-related tasks from that page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to appointments—such as creating, viewing, rescheduling, or cancelling—
            respond with a short, friendly, and informative message directing them to the Appointments page.
            Let them know they can manage and search for appointments there.
            Conclude the message by stating that there is a link below that will give them access to the Appointments page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_practice_location_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to practice locations.

    :param user_query: User's input related to practice location.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Practice Location page. "
        "Assume the user is looking to manage or edit their practice or clinic locations. "
        "Respond as an AI assistant and inform the admin that they can manage, update, or add new locations on the Practice Location page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to practice locations—such as managing clinics, adding new locations, or updating addresses—
            respond with a short and friendly message guiding them to the Practice Location page.
            Mention that they can view, edit, or add locations there.
            Conclude the message by stating that there is a link below to take them to the Practice Location management page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_contact_page_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to the contact page.

    :param user_query: User's input related to contacting support or the organization.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Contact page. "
        "Assume the user is looking to get in touch with support or the organization. "
        "Respond as an AI assistant and inform the admin that they can find contact information and support options on the Contact page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to contacting support or finding contact information,
            respond with a short and friendly message guiding them to the Contact page.
            Mention that they can find all necessary contact details and support options there.
            Conclude the message by stating that there is a link below to take them to the Contact page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_payer_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to payers.

    :param user_query: User's input related to payers.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Payer page. "
        "Assume the user is looking to manage or edit payer information."
        "Respond as an AI assistant and inform the admin that they can manage payer details on the Payer page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to payers—such as managing payer information or adding new payers—
            respond with a short and friendly message guiding them to the Payer page.
            Mention that they can view, edit, or add payer details there.
            Conclude the message by stating that there is a link below to take them to the Payer's page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_billing_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to billing.

    :param user_query: User's input related to billing.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Billing page. "
        "Assume the user is looking to manage or edit billing information. "
        "Respond as an AI assistant and inform the admin that they can manage billing details on the Billing page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to billing—such as managing invoices, payments, or billing settings—
            respond with a short and friendly message guiding them to the Billing page.
            Mention that they can view, edit, or manage all billing-related tasks there.
            Conclude the message by stating that there is a link below to take them to the Billing page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_Eprescription_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to e-prescriptions.

    :param user_query: User's input related to e-prescriptions.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the E-prescription page. "
        "Assume the user is looking to manage or edit e-prescriptions. "
        "Respond as an AI assistant and inform the admin that they can manage e-prescription details on the e-prescriptions page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform called.
            When an admin makes a query related to e-prescriptions—such as managing e-prescriptions or adding new ones—
            respond with a short and friendly message guiding them to the E-prescription page.
            Mention that they can view, edit, or manage all e-prescription-related tasks there.
            Conclude the message by stating that there is a link below to take them to the e-prescription page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_admin_settings_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to admin settings.

    :param user_query: User's input related to admin settings.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Admin Settings page. "
        "Mention that they can view, edit, or manage all admin tasks there."
        "Conclude the message by stating that there is a link below to take them to the Admin Settings page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to admin settings—such as managing user roles, permissions, or system settings—
            respond with a short and friendly message guiding them to the Admin Settings page.
            Mention that they can view, edit, or manage all admin-related tasks there.
            Conclude the message by stating that there is a link below to take them to the Admin Settings page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_billing_setting_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to billing settings.

    :param user_query: User's input related to billing settings.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Billing Settings page. "
        "Mention that they can view, edit, or manage all billing setting tasks there."
        "Conclude the message by stating that there is a link below to take them to the Billing Settings page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform called.
            When an admin makes a query related to billing settings—such as managing billing configurations, payment methods, or invoice settings—
            respond with a short and friendly message guiding them to the Billing Settings page.
            Mention that they can view, edit, or manage all billing-related settings there.
            Conclude the message by stating that there is a link below to take them to the Billing Settings page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_practice_settings_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to practice settings.

    :param user_query: User's input related to practice settings.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Practice Settings page. "
        "Mention that they can view, edit, or manage all practice setting tasks there."
        "Conclude the message by stating that there is a link below to take them to the Practice Settings page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to practice settings—such as managing practice information, configurations, or preferences—
            respond with a short and friendly message guiding them to the Practice Settings page.
            Mention that they can view, edit, or manage all practice-related settings there.
            Conclude the message by stating that there is a link below to take them to the Practice Settings page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
)

async def generate_payment_settings_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to payment settings.

    :param user_query: User's input related to payment settings.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Payment Settings page. "
        "Mention that they can view, edit, or manage all payment setting tasks there."
        "Conclude the message by stating that a link will be provided to take them to the Payment Settings page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to payment settings—such as managing payment methods, configurations, or preferences—
            respond with a short and friendly message guiding them to the Payment Settings page.
            Mention that they can view, edit, or manage all payment-related settings there.
            Conclude the message by stating that there is a link below to take them to the Payment Settings page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_manage_files_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a user request related to managing files.

    :param user_query: User's input related to file management.
    :param user_id: Unique identifier for the user.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from an admin:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the admin navigate to the Manage Files page. "
        "Mention that they can view, upload, or manage files there."
        "Conclude the message by informing them to use the link below to access the Manage Files page."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform.
            When an admin makes a query related to file management—such as uploading, viewing, or organizing files—
            respond with a short and friendly message guiding them to the Manage Files page.
            Mention that they can perform all file-related tasks there.
            Conclude the message by stating that a link will be provided to take them to the Manage Files page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

# >>>>>>>>>>>>>>>>>>>> Task functions for Clients  >>>>>>>>>>>>>>>>>>>>> 

async def generate_client_dashboard_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a client request related to the dashboard.

    :param user_query: Client's input related to the dashboard.
    :param user_id: Unique identifier for the client.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from a client:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the client navigate to their Dashboard. "
        "Assume they are looking to view their appointments, messages, or other personal information. "
        "Respond as an AI assistant and inform the client that they can access all their information on the Dashboard."
    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform for behavioural health services.
            Your role is to assist Clients in navigating to their dashboard.
            Based on their query, provide a short, friendly message guiding them to the main dashboard.
            Clearly confirm their intent and inform them to use the link below for quick access to the dashboard.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_client_appointment_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a client request related to appointments.

    :param user_query: Client's input related to appointments.
    :param user_id: Unique identifier for the client.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from a client:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the client navigate to their Appointments page. "
        "Assume they are looking to book an appointment with a healthcare provider, view upcoming appointments, or manage existing ones. "
        "Respond as an AI assistant and inform the client that they can access all their appointment information on the Appointments page."
    )
    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform for behavioural health services.
            Your role is to assist Clients in navigating to their appointments.
            Based on their query, provide a short, friendly message guiding them to the Appointments page.
            Clearly confirm their intent and inform them that a link will be available for quick access to the appointments page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_client_pratice_search_summary(   
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a client request related to practice search.

    :param user_query: Client's input related to practice search.
    :param user_id: Unique identifier for the client.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    user_prompt = (
        f"The following is a message from a client:\n"
        f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
        f"Query: '{user_query}'\n\n"
        "Based on the above query, generate a short, clear, and friendly response that helps the client navigate to their Practice Search page."
        "Assume they are looking to find a healthcare provider or practice and guide them accordingly."
        "Respond as an AI assistant and inform the client that they can search for practices or providers on the Practice Search page."

    )

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform for behavioural health services.
            Your role is to assist Clients in navigating to their practice search.
            Based on their query, provide a short, friendly message guiding them to the Practice Search page.
            Clearly confirm their intent and inform them that a link will be available for quick access to the practice search page.
        """,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )

async def generate_client_document_summary(
    user_query: str, 
    user_id: str,
    assistant_session_id: str,
    organization_id: str
) -> str:
    """
    Generates a friendly summary or navigation cue in response to a client request related to managing their documents.

    :param user_query: Client's input related to practice search.
    :param user_id: Unique identifier for the client.
    :param assistant_session_id: Session identifier for tracking the conversation.
    :param organization_id: Organization identifier for multi-tenancy support.
    :return: A concise AI-generated navigation message.
    """

    return await openai_generate_response_summary(
        system_prompt="""
            You are a helpful AI assistant for a telehealth platform for behavioural health services.
            Your role is to assist Clients in navigating to their documents.
            Based on their query, provide a short, friendly message guiding them to the Documents page.
            Clearly confirm their intent and inform them that a link will be available for quick access to the documents page.
        """,
        user_prompt=(
            f"The following is a message from a client:\n"
            f"User ID: {user_id}, Assistant Session ID: {assistant_session_id}, Organization ID: {organization_id}\n"
            f"Query: '{user_query}'\n\n"
            "Based on the above query, generate a short, clear, and friendly response that helps the client navigate to their Documents page. "
            "Assume they are looking to view or manage their personal documents or files. "
            "Respond as an AI assistant and inform the client that they can access all their document information on the Documents page."
        ),
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=300
    )