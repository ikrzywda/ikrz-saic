import math
from functools import reduce
from pathlib import Path

import rich
import typer
from pydantic import BaseModel, Field

# DFF := DayliannisFriendFilter

# Define SI prefixes dictionary as a constant
SI_PREFIXES = {
    -24: 'y',  # yocto
    -21: 'z',  # zepto
    -18: 'a',  # atto
    -15: 'f',  # femto
    -12: 'p',  # pico
    -9: 'n',   # nano
    -6: 'u',   # micro
    -3: 'm',   # milli
    0: '',     # (no prefix for base unit)
    3: 'k',    # kilo
    6: 'M',    # mega
    9: 'G',    # giga
    12: 'T',   # tera
    15: 'P',   # peta
    18: 'E',   # exa
    21: 'Z',   # zetta
    24: 'Y'    # yotta
}

def scientific_notation_to_str(value: float) -> str:
    magnitude = int(math.floor(math.log10(abs(value))))
    exponent = magnitude - (magnitude % 3)

    mantissa = value / (10 ** exponent)
    prefix = SI_PREFIXES.get(exponent, '')

    return f"{mantissa:g}{prefix}"

class DFFParams(BaseModel):
    f0: float = Field(..., alias="f0")
    Q: float = Field(..., alias="Q")
    K: float = Field(..., alias="K")
    R1: float = Field(..., alias="R1")
    C2: float = Field(..., alias="C2")
    R3: float = Field(..., alias="R3")
    C4: float = Field(..., alias="C4")
    R5: float = Field(..., alias="R5")
    R6: float = Field(..., alias="R6")


app = typer.Typer()


def insert_values_to_ltspice_model(model_buffer: str, **kwargs):
    replace_symbols = [key for key in kwargs.keys()]
    print(replace_symbols)
    lines_buffer = model_buffer.splitlines()
    for index, line in enumerate(lines_buffer):
        buf = []
        for c in line:
            buf.append(c)
        print(buf)
        if line.find("InstName") == -1:
            continue
        if index == len(lines_buffer) - 1:
            break
        next_line = lines_buffer[index + 1]
        print(next_line)
        if next_line.find("Value") == -1:
            continue


        for symbol in replace_symbols:
            if symbol in line:
                tokens_next_line = next_line.split()
                tokens_next_line[-1] = scientific_notation_to_str(kwargs[symbol])
                lines_buffer[index + 1] = " ".join(tokens_next_line)
                print(f"Replacing {symbol} with {scientific_notation_to_str(kwargs[symbol])}")
                break
        
    
    return reduce(lambda x, y: x + "\n" + y, lines_buffer)

def _compute_dff_params(
    f0: float = typer.Option(..., help="Frequency (f0)"),
    ku: float = typer.Option(..., help="Gain (K)"),
    q: float = typer.Option(..., help="Quality factor (Q)"),
    c: float = typer.Option(..., help="Capacitance (C)"),
) -> DFFParams:
    resistance_3 = q / (math.pi * f0 * c)
    resistance_6 = q / (2 * math.pi * f0 * c * ((2 * q ** 2) - abs(ku)))
    print(resistance_6 )
    resistance_5 = resistance_3
    resistance_1 = resistance_3 / (2 * abs(ku))

    capacitance_4 = c
    capacitance_2 = c

    return DFFParams(
        f0=f0,
        Q=q,
        K=ku,
        R1=resistance_1,
        C2=capacitance_2,
        R3=resistance_3,
        C4=capacitance_4,
        R5=resistance_5,
        R6=resistance_6,
    
)


@app.command()
def compute_dff_params_and_insert_into_ltspice_model(
    model_path: Path = typer.Argument(..., help="Path to LTSpice model"),
    f0: float = typer.Argument(..., help="Frequency (f0)"),
    ku: float = typer.Argument(..., help="Gain (K)"),
    q: float = typer.Argument(..., help="Quality factor (Q)"),
    c: float = typer.Argument(..., help="Capacitance (C)"),
) -> None:
    dff_params = _compute_dff_params(
        f0=f0, q=q, ku=ku, c=c,
    )
    with model_path.open("rb") as model_file:
        model_buffer = model_file.read().decode("latin-1")
        print(model_buffer)
        model_buffer = insert_values_to_ltspice_model(
            model_buffer,
            **dff_params.model_dump()
        )
    with model_path.open("w") as model_file:
        model_file.write(model_buffer.encode("latin-1").decode("utf-8"))

    typer.echo("Model updated!")
    rich.print_json(
        dff_params.model_dump_json(indent=2)
    )



@app.command()
def compute_dff_params(
    f0: float = typer.Argument(..., help="Frequency (f0)"),
    ku: float = typer.Argument(..., help="Gain (K)"),
    q: float = typer.Argument(..., help="Quality factor (Q)"),
    c: float = typer.Argument(..., help="Capacitance (C)"),
) -> DFFParams:
    rich.print_json(
        _compute_dff_params(
            f0=f0, q=q, ku=ku, c=c,
        ).model_dump_json(indent=2)
    )


if __name__ == "__main__":
    app()
