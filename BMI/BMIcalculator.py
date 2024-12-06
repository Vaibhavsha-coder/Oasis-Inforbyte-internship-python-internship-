import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class BMICalculator:
    def __init__(self, master):

        self.master = master
        self.master.title("Health Metrics Calculator")
        self.master.geometry("650x450")
        self.master.configure(bg="#f5f5f5")

        self.setup_ui()

    def setup_ui(self):

        # Create main container
        main_container = ttk.Frame(self.master, padding="25")
        main_container.pack(expand=True, fill="both")

        # Weight Section
        ttk.Label(main_container, text="Weight:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.weight_input = ttk.Entry(main_container, width=20)
        self.weight_input.grid(row=0, column=1, padx=5, pady=5)

        self.weight_unit_var = tk.StringVar(value="kgs")
        self.weight_unit_selector = ttk.Combobox(
            main_container, 
            textvariable=self.weight_unit_var, 
            values=("kgs", "lbs"), 
            state="readonly", 
            width=6
        )
        self.weight_unit_selector.grid(row=0, column=2, padx=5, pady=5)

        # Height Section
        ttk.Label(main_container, text="Height:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.height_input = ttk.Entry(main_container, width=20)
        self.height_input.grid(row=1, column=1, padx=5, pady=5)

        self.height_unit_var = tk.StringVar(value="meters")
        self.height_unit_selector = ttk.Combobox(
            main_container, 
            textvariable=self.height_unit_var, 
            values=("meters", "feet"), 
            state="readonly", 
            width=6
        )
        self.height_unit_selector.grid(row=1, column=2, padx=5, pady=5)

        # Calculate Button
        self.calculate_btn = ttk.Button(
            main_container, 
            text="Compute Health Metrics", 
            command=self.process_metrics
        )
        self.calculate_btn.grid(row=2, column=0, columnspan=3, pady=15)

        # Result Labels
        self.bmi_result_label = ttk.Label(main_container, text="BMI: ", font=("Arial", 12))
        self.bmi_result_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=5)

        self.category_result_label = ttk.Label(main_container, text="Health Category: ", font=("Arial", 12))
        self.category_result_label.grid(row=4, column=0, columnspan=3, sticky="w", pady=5)

        self.weight_range_label = ttk.Label(main_container, text="Recommended Weight Range: ", font=("Arial", 12))
        self.weight_range_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=5)

        self.height_range_label = ttk.Label(main_container, text="Recommended Height Range: ", font=("Arial", 12))
        self.height_range_label.grid(row=6, column=0, columnspan=3, sticky="w", pady=5)

    def calculate_bmi(self, weight: float, height: float) -> float:

        return weight / (height ** 2)

    def determine_health_category(self, bmi: float) -> str:

        categories = [
            (18.5, "Underweight"),
            (25, "Normal Weight"),
            (30, "Overweight"),
            (float('inf'), "Obese")
        ]
        
        return next(category for threshold, category in categories if bmi < threshold)

    def convert_units(self, value: float, unit: str, measurement_type: str) -> float:

        conversion_factors = {
            'weight': {'lbs': 0.453592, 'kgs': 1},
            'height': {'feet': 0.3048, 'meters': 1}
        }
        
        return value * conversion_factors[measurement_type].get(unit, 1)

    def compute_reference_ranges(self, height: float, weight: float) -> tuple:
 
        weight_range = (18.5 * (height ** 2), 24.9 * (height ** 2))
        height_range = ((weight / 24.9) ** 0.5, (weight / 18.5) ** 0.5)
        
        return weight_range, height_range

    def process_metrics(self):

        try:
            # Retrieve and convert inputs
            weight = float(self.weight_input.get())
            height = float(self.height_input.get())

            weight = self.convert_units(weight, self.weight_unit_var.get(), 'weight')
            height = self.convert_units(height, self.height_unit_var.get(), 'height')

            # Calculate metrics
            bmi_value = self.calculate_bmi(weight, height)
            health_category = self.determine_health_category(bmi_value)
            weight_range, height_range = self.compute_reference_ranges(height, weight)

            # Update result labels
            self.bmi_result_label.config(text=f"BMI: {bmi_value:.2f}")
            self.category_result_label.config(text=f"Health Category: {health_category}")
            self.weight_range_label.config(text=f"Recommended Weight Range: {weight_range[0]:.2f} - {weight_range[1]:.2f} kg")
            self.height_range_label.config(text=f"Recommended Height Range: {height_range[0]:.2f} - {height_range[1]:.2f} m")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values")

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()