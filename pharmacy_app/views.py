from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicine, MedicineCategory, MedicineUnit


class Index(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


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
                medicine.count = MedicineUnit.objects.filter(medicine=medicine).count()
                medicine.save()
            return Medicine.objects.all()


class MedicinesDetailView(LoginRequiredMixin, DetailView):
    template_name = "medicines_detail.html"
    model = Medicine
