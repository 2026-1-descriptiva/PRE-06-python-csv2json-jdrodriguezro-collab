"""Script para convertir un archivo CSV a JSON 1"""

import csv
import json
from pathlib import Path

from nicegui import ui


def convert_csv_2_json(input_file):
    """Converts a CSV file to a JSON file."""

    if not input_file:
        ui.notify("Por favor ingresa el nombre del archivo CSV.")
        return

    csv_path = Path(input_file)
    project_root = Path(__file__).resolve().parents[1]

    if not csv_path.is_absolute():
        candidate = project_root / "files" / csv_path
        if candidate.exists():
            csv_path = candidate
        elif csv_path.suffix.lower() != ".csv":
            csv_path = csv_path.with_suffix(".csv")
            candidate = project_root / "files" / csv_path.name
            if candidate.exists():
                csv_path = candidate

    if csv_path.suffix.lower() != ".csv":
        csv_path = csv_path.with_suffix(".csv")

    if not csv_path.exists():
        ui.notify(f"Archivo no encontrado: {csv_path}")
        return

    output_path = csv_path.with_suffix(".json")
    data = []

    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        ui.notify(f"Archivo convertido correctamente: {output_path}")
    except Exception as error:
        ui.notify(f"Error al convertir: {error}")


def app():
    """Main function to run the app"""

    ui.label("CSV to JSON Converter").classes("text-4xl font-bold")
    ui.label("")

    filename = ui.input(
        label="CSV file to convert:",
        placeholder="files/drivers.csv",
    )

    ui.label("")

    ui.label("")
    ui.button("Convert", on_click=lambda: convert_csv_2_json(filename.value))
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    app()