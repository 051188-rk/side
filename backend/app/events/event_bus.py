"""
Event Bus for decoupled event handling

This module provides a simple event bus for publishing and subscribing to events
within the application, enabling loose coupling between components.
"""

from typing import Callable, Dict, List, Any, Optional
from asyncio import Queue, Event, create_task
import asyncio
from app.core.logging import log


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_queue: Queue = Queue()
        self._running = False
        self._worker_task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the event bus worker."""
        if self._running:
            return
        
        self._running = True
        self._worker_task = create_task(self._process_events())
        log.info("Event bus started")

    async def stop(self):
        """Stop the event bus worker."""
        if not self._running:
            return
        
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        log.info("Event bus stopped")

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        log.info(f"Subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            if handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
                log.info(f"Unsubscribed from event: {event_type}")

    async def publish(self, event_type: str, data: Any):
        """Publish an event to the event bus."""
        await self._event_queue.put({
            "type": event_type,
            "data": data,
        })
        log.debug(f"Published event: {event_type}")

    async def _process_events(self):
        """Process events from the queue."""
        while self._running:
            try:
                event = await self._event_queue.get()
                await self._handle_event(event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error(f"Error processing event: {e}")

    async def _handle_event(self, event: Dict[str, Any]):
        """Handle a single event by notifying all subscribers."""
        event_type = event["type"]
        data = event["data"]
        
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                log.error(f"Error in event handler for {event_type}: {e}")


# Global event bus instance
event_bus = EventBus()
