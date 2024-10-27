from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import BMICalculator
from .forms import BMICalculatorForm
from groq import Groq
import os
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def Bmi(request):
    bmi = None
    bmi_category = None
    gender = None

    if request.method == "POST":
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            bmi_instance = form.save(commit=False)
            bmi_instance.user = request.user
            bmi_instance.save()

            bmi = bmi_instance.bmi
            gender = request.POST.get("gender")
            print("gender", gender)

            if bmi is not None:
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
            prompt = (
                f"give me just i want short information about the best diet plan "
                f"recommendation for {bmi} BMI in 3 line (give me how many calories "
                f"I should eat for man) and with example of exercises"
            )
        else:
            prompt = (
                f"give me just i want short information about the best diet plan "
                f"recommendation for {bmi} BMI in 3 line (give me how many calories "
                f"I should eat for woman) and with example of exercises"
            )

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        advice = chat_completion.choices[0].message.content

        response_data = {
            "bmi": bmi,
            "bmi_category": bmi_category,
            "advice": advice,
        }

        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request method."}, status=400)


def ListBmi(request):

    bmi_list = BMICalculator.objects.filter(user=request.user)

    bmi_records = []
    for bmi in bmi_list:

        if bmi.bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi.bmi < 25:
            bmi_category = "Healthy"
        elif 25 <= bmi.bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        bmi_records.append(
            {
                "id": bmi.id,
                "bmi": bmi.bmi,
                "weight": bmi.weight,
                "height": bmi.height,
                "age": bmi.age,
                "gender": bmi.gender,
                "category": bmi_category,
            }
        )

    paginator = Paginator(bmi_records, 5)
    page_number = request.GET.get("page")
    paginated_bmi_records = paginator.get_page(page_number)

    return render(request, "bmi_list.html", {"bmi_records": paginated_bmi_records})


def get_bmi_by_id(request, id):
    try:

        bmi_record = BMICalculator.objects.get(id=id)
        print("Retrieved BMI Record:", bmi_record)

        if bmi_record.bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi_record.bmi < 25:
            bmi_category = "Healthy"
        elif 25 <= bmi_record.bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        return render(
            request,
            "bmi_details.html",
            {"bmi_record": bmi_record, "bmi_category": bmi_category},
        )

    except BMICalculator.DoesNotExist:
        raise Http404("BMI record not found.")


def update_bmi(request, id):
    bmi_record = get_object_or_404(BMICalculator, id=id)
    bmi = None
    bmi_category = None

    if request.method == "POST":
        form = BMICalculatorForm(request.POST, instance=bmi_record)
        if form.is_valid():

            bmi_instance = form.save()

            bmi = bmi_instance.bmi
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_category = "Healthy"
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"

            return redirect("bmi_details", id=id)
    else:
        form = BMICalculatorForm(instance=bmi_record)
        bmi = bmi_record.bmi

        if bmi is not None:
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_category = "Healthy"
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"

    return render(
        request,
        "bmi_details.html",
        {
            "form": form,
            "bmi_record": bmi_record,
            "bmi": bmi,
            "bmi_category": bmi_category,
        },
    )


def delete_bmi(request, id):
    bmi_record = get_object_or_404(BMICalculator, id=id)

    if request.method == "POST":
        bmi_record.delete()
        messages.success(request, "BMI record deleted successfully.")
        return redirect("list_bmi")

    return redirect("list_bmi")
