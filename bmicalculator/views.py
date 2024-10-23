from django.shortcuts import render, get_object_or_404, redirect
from .models import BMICalculator
from .forms import BMICalculatorForm
from groq import Groq
import os

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def Bmi(request):
    bmi = None
    bmi_category = None
    gender = None
    if request.method == "POST":
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            bmi_instance = form.save()
            bmi = bmi_instance.bmi
            gender = request.POST.get("gender")
            print("gender", gender)

            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_category = "Healthy"
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"
    else:
        form = BMICalculatorForm()

    return render(
        request,
        "bmi-calculator.html",
        {"form": form, "bmi": bmi, "bmi_category": bmi_category, "gender": gender},
    )


def get_advice(request):
    if request.method == "POST":
        bmi = request.POST.get("bmi")
        gender = request.POST.get("gender")
        bmi_category = request.POST.get("bmi_category")

        if gender == "M":
            prompt = f"give me just i want short information about the best diet plan recommendation for {bmi} BMI in 3 line (give me how many calories i should eat for man ) and with example of exercies"
        else:
            prompt = f"give me just i want short information about the best diet plan recommendation for {bmi} BMI in 3 line (give me how many calories i should eat for woman ) and with example of  exercies"

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        advice = chat_completion.choices[0].message.content

        form = BMICalculatorForm(request.POST)
        return render(
            request,
            "bmi-calculator.html",
            {
                "form": form,
                "bmi": bmi,
                "advice": advice,
                "bmi_category": bmi_category,
            },
        )

    return redirect("bmi_calculator")
