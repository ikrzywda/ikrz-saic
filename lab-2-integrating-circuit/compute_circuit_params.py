import rich
import typer
from pydantic import BaseModel


class CircuitParams(BaseModel):
    input_amplitude: float
    output_amplitude: float
    frequency: float
    capacitance: float
    resistance: float
    resistance_1: float
    generator_resistance: float
    compensating_resistance: float

def compute_circuit_params(
    *,
    input_amplitude: float,
    output_amplitude: float,
    frequency: float,
    generator_resistance: float,
    capacitance: float,
) -> CircuitParams:
    
    resistance = input_amplitude / (4 * output_amplitude * frequency * capacitance)
    resistance_1 = 120_000

    compensating_resistance = ((generator_resistance + resistance) * resistance_1) / (generator_resistance + resistance + resistance_1)

    return CircuitParams(
        input_amplitude=input_amplitude,
        output_amplitude=output_amplitude,
        frequency=frequency,
        capacitance=capacitance,
        resistance=resistance,
        resistance_1=resistance_1,
        generator_resistance=generator_resistance,
        compensating_resistance=compensating_resistance,
    )

app = typer.Typer()

@app.command()
def main(
    input_amplitude: float = typer.Option(..., help="Input amplitude (U_wem)"),
    output_amplitude: float = typer.Option(..., help="Output amplitude (U_wym)"),
    frequency: float = typer.Option(..., help="Frequency (f)"),
    generator_resistance: float = typer.Option(..., help="Generator resistance (R_G)"),
    capacitance: float = typer.Option(..., help="Capacitance (C)"),
):
    circuit_params = compute_circuit_params(
        input_amplitude=input_amplitude,
        output_amplitude=output_amplitude,
        frequency=frequency,
        generator_resistance=generator_resistance,
        capacitance=capacitance,
    )
    rich.print(circuit_params.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
