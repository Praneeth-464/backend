from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from ..schemas import EmergencyContactCreate, EmergencyContactResponse
from ..crud import create_emergency_contact, get_emergency_contacts, get_primary_emergency_contact, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/", response_model=EmergencyContactResponse)
async def create_emergency_contact_endpoint(contact: EmergencyContactCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create an emergency contact for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        emergency_contact = create_emergency_contact(
            user.id,
            contact.name,
            contact.phone,
            contact.relationship,
            contact.is_primary or False
        )
        
        if not emergency_contact:
            raise HTTPException(status_code=500, detail="Error creating emergency contact")
        
        return simple_datetime_handler(emergency_contact)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_emergency_contact_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating emergency contact: {str(e)}")

@router.get("/", response_model=list[EmergencyContactResponse])
async def get_emergency_contacts_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get all emergency contacts for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        contacts = get_emergency_contacts(user.id)
        return simple_datetime_handler(contacts)
    except Exception as e:
        print(f"Error in get_emergency_contacts_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving emergency contacts: {str(e)}")

@router.get("/primary", response_model=EmergencyContactResponse)
async def get_primary_emergency_contact_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get the primary emergency contact for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        contact = get_primary_emergency_contact(user.id)
        if not contact:
            raise HTTPException(status_code=404, detail="Primary emergency contact not found")
        
        return simple_datetime_handler(contact)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_primary_emergency_contact_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving primary emergency contact: {str(e)}")