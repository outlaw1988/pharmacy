from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicine, MedicineCategory, MedicineUnit, MedicineSale
from .forms import SalesForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from pharmacy.tasks import *


class Index(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def post(self, request):

        if "add-medicines" in request.POST:
            add_medicines.delay()
        elif "add-stock" in request.POST:
            add_to_stock.delay()
        elif "generate-sales" in request.POST:
            generate_sales.delay()

        return HttpResponseRedirect(reverse('index'))


class MedicinesList(LoginRequiredMixin, ListView):
    template_name = "medicines_list.html"
    model = Medicine

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        categories = MedicineCategory.objects.all()
        data['categories'] = categories
        return data

    def get_queryset(self):
        if "category" in self.kwargs:
            category = MedicineCategory.objects.filter(name=self.kwargs['category'])[0]
            self.request.session['category'] = category.name
            return Medicine.objects.filter(category=category)
        if "ordering" in self.kwargs:
            if self.request.session['category'] == "all":
                return Medicine.objects.all().order_by(self.kwargs['ordering'])
            else:
                category_name = self.request.session['category']
                category = MedicineCategory.objects.filter(name=category_name)[0]
                return Medicine.objects.filter(category=category).order_by(self.kwargs['ordering'])
        else:
            self.request.session['category'] = "all"
            medicines = Medicine.objects.all()
            for medicine in medicines:
                medicine.count = MedicineUnit.objects.filter(medicine=medicine,
                                                             status='a').count()
                medicine.save()
            return Medicine.objects.all()


class MedicinesDetailView(LoginRequiredMixin, DetailView):
    template_name = "medicines_detail.html"
    model = Medicine


class Sales(LoginRequiredMixin, TemplateView):
    template_name = "sales.html"

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            # GET request
            form = SalesForm()
        else:
            # POST request
            form = kwargs['form']

        context = {
            'form': form
        }
        return context

    def post(self, request):
        print("POST request: ", request.POST)
        # Important: request POST is required!!!!
        form = SalesForm(request.POST)
        if form.is_valid():
            # self.form_valid(request)
            count = int(request.POST['count'])
            medicine_id = request.POST['medicine']
            medicine = Medicine.objects.filter(id=medicine_id)[0]
            medicine_units = MedicineUnit.objects.filter(medicine=medicine, status='a')
            print("Medicine units: ", medicine_units)
            # for i in range(count):
            #     print("I: ", i)
            #     medicine_units[i].status = 's'
            #     medicine_units[i].save()
            counter = 0
            for medicine_unit in medicine_units:
                counter += 1
                if counter > count:
                    break
                medicine_unit.status = 's'
                medicine_unit.save()

            amount = float(count) * medicine.price
            now = datetime.datetime.now()
            today_date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
            today_time = "{0}:{1}".format(now.hour, now.minute)
            sale = MedicineSale(medicine=medicine, items_count=count, amount=amount,
                                purchase_date=today_date, purchase_time=today_time)
            sale.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context=context)


class SalesList(LoginRequiredMixin, ListView):

    template_name = "sales_list.html"
    model = MedicineSale
