from django.shortcuts import render, get_object_or_404, redirect
from .models import BMICalculator
from .forms import BMICalculatorForm


def Bmi(request):
    bmi = None  # Initialize BMI to None
    if request.method == "POST":
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            bmi_instance = form.save()  # Save the form data
            bmi = bmi_instance.bmi  # Get the calculated BMI
    else:
        form = BMICalculatorForm()

    # Render the template with both form and BMI result
    return render(request, "bmi-calculator.html", {"form": form, "bmi": bmi})


# List all BMI records
def bmi_list(request):
    bmi_list = BMICalculator.objects.all()
    return render(request, "bmi_list.html", {"bmi_list": bmi_list})


# Update an existing BMI record
def bmi_update(request, pk):
    bmi_record = get_object_or_404(BMICalculator, pk=pk)
    if request.method == "POST":
        form = BMICalculatorForm(request.POST, instance=bmi_record)
        if form.is_valid():
            form.save()
            return redirect("bmi_list")  # Redirect to list after updating
    else:
        form = BMICalculatorForm(instance=bmi_record)
    return render(request, "bmi_update.html", {"form": form, "bmi_record": bmi_record})


# Delete a BMI record
def bmi_delete(request, pk):
    bmi_record = get_object_or_404(BMICalculator, pk=pk)
    if request.method == "POST":
        bmi_record.delete()
        return redirect("bmi_list")
    return render(request, "bmi_delete.html", {"bmi_record": bmi_record})
