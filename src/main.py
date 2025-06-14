import io
import zipfile

import litserve as ls
from pydantic import BaseModel

from fastapi.responses import Response
from planning import PlanningAgent
from analyzing import AnalizeAgent
from coding import CodingAgent


class Paper(BaseModel):  # Validación súper simple del texto del paper en json
    """
    Esta validación posiblemente solo sirva para mandar requests con JSON mediante Swagger
    """
    text: str


class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        self.planning_agent = PlanningAgent()
        self.analize_agent = AnalizeAgent()
        self.coding_agent = CodingAgent()

    async def decode_request(self, request: Paper, **kwargs):
        return request.text  # Todo el contenido del paper en formato JSON

    async def predict(self, x, **kwargs):
        # Primer paso, planning
        planning_results = self.planning_agent.process_data(x)
        # analize toma los resultados de planning
        analize_results = self.analize_agent.process_data(planning_results)
        # coding toma los resultados de analize
        coding_results = self.coding_agent.process_data(analize_results)
        return coding_results

    async def encode_response(self, output, **kwargs):
        """
        Convierte la salida del coding agent en un zip
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            zipf.writestr('output.py', output)
        zip_buffer.seek(0)
        return Response(
            zip_buffer.read(),
            headers={"Content-Disposition": "attachment; filename=output.zip"},
            media_type="application/zip"
        )


if __name__ == "__main__":
    api = SimpleLitAPI(enable_async=True)
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8000, generate_client_file=False)
