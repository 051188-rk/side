from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.ticket import TicketResponse, TicketCreate, TicketUpdate, TicketStatusUpdate
from app.schemas.ticket_update import TicketUpdateCreate
from app.schemas.common import SuccessResponse
from app.repositories.ticket_repository import TicketRepository
from app.repositories.ticket_update_repository import TicketUpdateRepository
from app.core.security import get_current_user, require_user
from app.core.logging import log

router = APIRouter()
ticket_repo = TicketRepository()
ticket_update_repo = TicketUpdateRepository()


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: dict = Depends(get_current_user)
):
    ticket_id = await ticket_repo.create_ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category,
        severity=ticket_data.severity,
        priority_score=ticket_data.priority_score,
        suggested_owner=ticket_data.suggested_owner,
        labels=ticket_data.labels,
        affected_feature=ticket_data.affected_feature,
        reproduction_steps=ticket_data.reproduction_steps,
        related_tickets=ticket_data.related_tickets,
        organization_id=ticket_data.organization_id
    )
    ticket = await ticket_repo.get_by_id(ticket_id)
    return ticket


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    current_user: dict = Depends(require_user())
):
    ticket = await ticket_repo.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    updates: TicketUpdate,
    current_user: dict = Depends(require_user())
):
    await ticket_repo.update(ticket_id, updates.dict(exclude_unset=True))
    ticket = await ticket_repo.get_by_id(ticket_id)
    return ticket


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(
    ticket_id: str,
    status_update: TicketStatusUpdate,
    current_user: dict = Depends(require_user())
):
    if status_update.status:
        await ticket_repo.update_status(ticket_id, status_update.status)
    if status_update.assignee:
        await ticket_repo.assign_ticket(ticket_id, status_update.assignee)
    if status_update.resolution:
        await ticket_repo.resolve_ticket(ticket_id, status_update.resolution)
    
    ticket = await ticket_repo.get_by_id(ticket_id)
    return ticket


@router.post("/{ticket_id}/updates", response_model=SuccessResponse)
async def add_ticket_update(
    ticket_id: str,
    update_data: TicketUpdateCreate,
    current_user: dict = Depends(require_user())
):
    update_id = await ticket_update_repo.create_update(
        ticket_id=ticket_id,
        author_id=current_user["user_id"],
        content=update_data.content,
        update_type=update_data.update_type
    )
    return SuccessResponse(
        success=True,
        message="Ticket update added",
        data={"update_id": update_id}
    )


@router.get("/{ticket_id}/updates", response_model=List)
async def get_ticket_updates(
    ticket_id: str,
    current_user: dict = Depends(require_user())
):
    updates = await ticket_update_repo.get_by_ticket(ticket_id)
    return updates


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    limit: int = 100,
    offset: int = 0,
    status: str = None,
    category: str = None,
    current_user: dict = Depends(require_user())
):
    if status:
        tickets = await ticket_repo.get_by_status(status, limit=limit)
    elif category:
        tickets = await ticket_repo.get_by_category(category, limit=limit)
    else:
        tickets = await ticket_repo.list_all(limit=limit, offset=offset)
    return tickets


@router.get("/high-priority", response_model=List[TicketResponse])
async def get_high_priority_tickets(
    min_score: float = 0.7,
    limit: int = 50,
    current_user: dict = Depends(require_user())
):
    tickets = await ticket_repo.get_high_priority(min_score=min_score, limit=limit)
    return tickets
