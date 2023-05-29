from django.shortcuts import render
from .serializer import CSVUploadSerializer, SinglefieldSerializer
import csv
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
from django.core.files.storage import default_storage
from rest_framework import status
import time
from .models import *
from .utils.sender import *
from .utils.consumer import *
from rest_framework.permissions import  IsAuthenticated

class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CSVUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = request.FILES['csv_file']
            file_name = default_storage.save(file.name, file)
            print("file saved in default storage-----")
            data = pd.read_csv(file_name)
            return Response({'message': data.columns},status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileProcessing(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        column_name = request.data["email_field"]
        file_name = request.data["file_name"]
        print(column_name,file_name) 
        start = time.time()
        file = default_storage.open(file_name)
        counter = 0
        df = pd.read_csv(file)
        publish_bulk(df[column_name].to_json())
        print("file send to queue")
        a = consume_email()
        print(a,'consumed data')          
        return Response({"total execution time":time.time()-start, "message": a},status= status.HTTP_200_OK)

class SingleFileProcessing(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SinglefieldSerializer
    def post(self,request):    
        serializer = self.serializer_class(data = request.data)       
        if serializer.is_valid():
            print(type(request.data["email"]))
            publish_go(request.data["email"])
            result = consume_single_email()
            # account_balance = request.balance
            # verified_email = SingleEmaillist.objects.create(data=result)
            # updated_account = Account_Balance.objects.update(initial_balance=account_balance)
            return Response({"message":result, "account_balance":'test'}, status= status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

