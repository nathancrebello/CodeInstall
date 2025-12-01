"""
AI-powered installation assistant using OpenAI API.
"""
import re
import logging
import time
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class AIAssistant:
    """Handles AI-powered code generation for software downloads."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", instructions: str = ""):
        """
        Initialize the AI assistant.

        Args:
            api_key: OpenAI API key
            model: Model to use for generation
            instructions: System instructions for the assistant
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.instructions = instructions
        logger.info(f"AI Assistant initialized with model: {model}")

    def generate_download_script(self, user_prompt: str) -> Optional[str]:
        """
        Generate a Python script to download software based on user input.

        Args:
            user_prompt: User's request (e.g., "download Python")

        Returns:
            Generated Python code as string, or None if generation failed
        """
        try:
            logger.info(f"Generating download script for: {user_prompt}")

            # Create assistant
            assistant = self.client.beta.assistants.create(
                name="Installation Assistant",
                instructions=self.instructions,
                tools=[{"type": "code_interpreter"}],
                model=self.model
            )

            # Create thread and message
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt
            )

            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                time.sleep(1)

            if run.status != 'completed':
                logger.error(f"Assistant run failed with status: {run.status}")
                return None

            # Retrieve messages
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)

            # Extract assistant's response
            for message in reversed(messages.data):
                if message.role == "assistant":
                    response = message.content[0].text.value
                    logger.debug(f"Assistant response: {response[:200]}...")

                    # Extract Python code from markdown
                    code = self._extract_python_code(response)
                    if code:
                        logger.info("Successfully generated download script")
                        return code

            logger.warning("No Python code found in assistant response")
            return None

        except Exception as e:
            logger.error(f"Error generating download script: {e}")
            return None

    def _extract_python_code(self, response: str) -> Optional[str]:
        """
        Extract Python code from markdown code blocks.

        Args:
            response: Assistant's response text

        Returns:
            Extracted Python code or None
        """
        # Try to extract code between ```python and ```
        match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try generic code blocks
        match = re.search(r"```\n(.*?)```", response, re.DOTALL)
        if match:
            return match.group(1).strip()

        logger.warning("Could not extract Python code from response")
        return None

    def extract_required_modules(self, code: str) -> list[str]:
        """
        Extract imported modules from Python code.

        Args:
            code: Python code as string

        Returns:
            List of module names to install
        """
        lines = code.split('\n')
        modules = []

        for line in lines:
            line = line.strip()
            if line.startswith('import '):
                module = line.split()[1].split('.')[0]
                modules.append(module)
            elif line.startswith('from '):
                module = line.split()[1].split('.')[0]
                modules.append(module)

        logger.info(f"Extracted modules: {modules}")
        return modules
