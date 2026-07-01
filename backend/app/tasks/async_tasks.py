"""
Async task definitions

This module defines async tasks that can be executed by background workers.
"""

import asyncio
from typing import Callable, Any, Dict
from app.core.logging import log


class AsyncTask:
    """Base class for async tasks."""
    
    def __init__(self, name: str, func: Callable, max_retries: int = 3):
        self.name = name
        self.func = func
        self.max_retries = max_retries
        self.retry_count = 0

    async def execute(self, *args, **kwargs) -> Any:
        """Execute the task with retry logic."""
        while self.retry_count <= self.max_retries:
            try:
                result = await self.func(*args, **kwargs)
                self.retry_count = 0  # Reset on success
                return result
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    log.error(f"Task {self.name} failed after {self.max_retries} retries: {e}")
                    raise
                log.warning(f"Task {self.name} failed (attempt {self.retry_count}/{self.max_retries}), retrying...")
                await asyncio.sleep(2 ** self.retry_count)  # Exponential backoff


class TaskQueue:
    """Async task queue for background processing."""
    
    def __init__(self, max_size: int = 1000):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self.running = False
        self.workers: list = []

    async def start(self, num_workers: int = 4):
        """Start the task queue with workers."""
        self.running = True
        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
        log.info(f"Started {num_workers} task queue workers")

    async def stop(self):
        """Stop the task queue workers."""
        self.running = False
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        log.info("Stopped task queue workers")

    async def enqueue(self, task: AsyncTask):
        """Enqueue a task for processing."""
        await self.queue.put(task)
        log.debug(f"Enqueued task: {task.name}")

    async def _worker(self, worker_name: str):
        """Worker that processes tasks from the queue."""
        while self.running:
            try:
                task = await self.queue.get()
                log.info(f"{worker_name} processing task: {task.name}")
                await task.execute()
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error(f"{worker_name} error processing task: {e}")


# Global task queue
task_queue = TaskQueue()
