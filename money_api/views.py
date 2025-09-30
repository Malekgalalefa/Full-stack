from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.models import User
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer
import openpyxl

class UploadFinance(APIView):
    def post(self, request, user_id, year):
        # 1. Check user exists
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Check file
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        if not (file.name.endswith('.xlsx') or file.name.endswith('.xls')):
            return Response({'error': 'Invalid file type. Use .xlsx or .xls'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Load workbook
        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
            header = [cell.value.lower() for cell in sheet[1]]

            # 4. Check required columns
            try:
                month_idx = header.index('month')
                amount_idx = header.index('amount')
            except ValueError:
                return Response({'error': 'Missing "Month" or "Amount" column'}, status=status.HTTP_400_BAD_REQUEST)

            # 5. Month mapping (for names)
            month_map = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
            }

            records = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Handle month
                month_value = row[month_idx]
                if isinstance(month_value, int):
                    month = month_value
                elif isinstance(month_value, str):
                    month = month_map.get(month_value.strip().lower())
                else:
                    month = None

                if not month or month < 1 or month > 12:
                    return Response({'error': f'Invalid month value: {row[month_idx]}'}, status=status.HTTP_400_BAD_REQUEST)

                # Handle amount
                try:
                    amount = float(row[amount_idx])
                except:
                    return Response({'error': f'Invalid amount value: {row[amount_idx]}'}, status=status.HTTP_400_BAD_REQUEST)

                records.append(FinancialRecord(user=user, year=year, month=month, amount=amount))

            # 6. Save to DB (overwrite existing for user/year)
            with transaction.atomic():
                FinancialRecord.objects.filter(user=user, year=year).delete()
                FinancialRecord.objects.bulk_create(records)

            return Response({'message': 'Financial data successfully stored', 'inserted': len(records)}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetFinance(APIView):
    def get(self, request, user_id, year):
        records = FinancialRecord.objects.filter(user_id=user_id, year=year).order_by('month')
        serializer = FinancialRecordSerializer(records, many=True)
        return Response(serializer.data)


from django.shortcuts import render

# Dashboard view
def finance_dashboard(request):
    """
    Render the finance dashboard template.
    """
    return render(request, 'money_api/index.html')

from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Finance API. Use /upload/<user_id>/<year>/ or /records/<user_id>/<year>/"
    })
