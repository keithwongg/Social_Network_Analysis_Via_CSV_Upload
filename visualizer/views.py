from django.shortcuts import render
import csv, io, json, numpy, scipy, random, os
from .models import Referral
# from networkanalysis.settings import BASE_DIR
import networkx as nx
from itertools import islice
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_export_file_path = BASE_DIR+ '/networkanalysis/static/csv/data_export.csv'
## Reset CSV function is used in other request functions, so it will have to be placed in the Global scope.
def reset_csv():
    print('yeah its resetting csv')
    headers_csv = [
        "Advocate_First_Name",
        "Advocate_Last_Name",
        "Advocate_Email", 
        "Advocate_Name",
        "Friend_First_Name",
        "Friend_Last_Name",
        "Friend_Name",
        "Friend_Email", 
        "Order_Number",
        "Completed_At", 
        "State", 
        "Total_Amount_Spent"]
    with open(data_export_file_path, 'w') as outfile:
        writer = csv.writer(outfile, delimiter = ',')
        writer.writerow(headers_csv)

def upload_csv(request):
    '''
    Write data to DB (Django model). Redirect to analytics url to parse graph data to front-end hidden para element, where renderGraph()
    function in renderGraph.js renders the graph within the container.

    Try Except: to send alert for wrong date format. Re-upload required.
    IF date_empty: to send alert that some date fields are empty and will be replaced with current datetime.
    IF Total Amount spent is empty: fill in the blanks with 0.00. 

    '''
    if "GET" == request.method:
        return render(request, "upload_csv.html", {'message': "Upload your CSV file here"})
    # if not GET, then proceed
    if "POST" == request.method:
        csv_file = request.FILES["csv_file"]
        # csv_file2 = request.FILES["csv_file2"]
        if not csv_file.name.endswith('.csv'):
            return render(request, "upload_csv.html", {'message' : "First Upload is not a CSV file. Please reupload the file."})
        # if not csv_file2.name.endswith('.csv'):
        #     return render(request, "upload_csv.html", {'message' : "Second Upload is not a CSV file. Please reupload the file."})

        Referral.objects.all().delete()

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        ## To write data to Json within static/js
        data_in_json = {}
        data_in_json['nodes'] = []
        data_in_json['edges'] = []
        group_number = 0

        # Test if date got empty fields 
        date_empty = False
        basket_empty = False
        order_number_missing = False

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                model = Referral()

                if len(column[6]) == 0:
                    return render(request, 'upload_csv.html', {"wrong_format_value_error": False, "order_number_missing": True, "csv_empty": False})
                if len(column[7][:10]) == 0:
                    date_empty = True
                if len(column[9]) == 0:
                    basket_empty = True

                model.Advocate_First_Name = column[0]
                model.Advocate_Last_Name = column[1]
                model.Advocate_Name = column[0] + ' ' + column[1]
                model.Advocate_Email = column[2]
                model.Friend_First_Name = column[3]
                model.Friend_Last_Name = column[4]
                model.Friend_Name = column[3] + ' ' + column[4]
                model.Friend_Email = column[5]
                model.Order_Number = column[6]
                model.Completed_At = datetime.strptime(column[7][:10] , '%Y-%m-%d') if len(column[7][:10]) != 0 else datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                model.State = column[8]
                model.Total_Amount_Spent = float(column[9]) if len(column[9]) != 0 else '0.00'
                model.save()
            # handle (ValueError, AttributeError, IndexError)
            except:
                return render(request, 'upload_csv.html', {"wrong_format_value_error": True, "order_number_missing": False, "csv_empty": False})

        if date_empty and basket_empty:
            return render(request, 'analytics.html', {"date_empty": True, "basket_empty": True})
        elif date_empty:
            return render(request, 'analytics.html', {"date_empty": True, "basket_empty": False})
        elif basket_empty:
            return render(request, 'analytics.html', {"date_empty": False, "basket_empty": True})

        return redirect('analytics/')


def analytics(request):
    def load_data_to_display(date_filter=["2010-01-01", "2030-01-01"]):
        ''' 
        date_filter params by default are set in a way to allow for all data to load on the graph upon the first upload without 
        activating any date filters. Hence the 2010 to 2030 time frame.
        '''
        data_to_display = {"nodes":[], "edges":[]}
        data = serializers.serialize('json', Referral.objects.filter(Completed_At__gte= date_filter[0], Completed_At__lte= date_filter[1]))
        data = json.loads(data)

        edge_reverse_dict = {} # initalize reverse dict (see below for more details)

        # Note: Havnet check for null names
        for line in data:
            fields = line["fields"]
            advocate_name = fields["Advocate_Name"]
            friend_name = fields["Friend_Name"]
            basket_weight = fields["Total_Amount_Spent"]
            # Add Nodes
            if len(data_to_display['nodes']) == 0:
                data_to_display['nodes'].append({
                    "id": advocate_name,
                })
            else:
                nodes_list = [name for node in data_to_display['nodes'] for key, name in node.items()]
                if advocate_name not in nodes_list:
                    data_to_display['nodes'].append({
                    "id": advocate_name,
                })
                if friend_name not in nodes_list:
                    data_to_display['nodes'].append({
                    "id": friend_name,
                })
            
            ## Add Edges
            '''
            There might be edges with the same 'from' and 'to'. However, AnyChart framework only allows unique edges.
            Hence, for edges that falls within this category, they will be added to the basket weight. By creating and
            using a reverse dictionay, it reduces search times if we were just to use for loops.
            
            Complexity: O(n) for creation, subsequent search time will be O(1)
            reverse dict key : combination of 'from' and 'to' --> unique (no duplicates)
            If edge alr exist, add current edge basket value to existing basket value.

            At the end of everything, get all the values of the dict and pump it into the actual edge list to display. O(n).
            '''
            edge_to_append = {
                "from": advocate_name,
                "to": friend_name,
                "normal": {
                    "stroke":  {
                        "color": "#A3D2FA",
                        "thickness": str(int(float(basket_weight)/20)),
                    }
                },
                "hovered": {
                    "stroke": {
                        "color": "black",
                        "thickness": str(int(float(basket_weight)/20)),
                    }
                },
                "selected": {"stroke": f'{str(int(float(basket_weight)*1.75/20))} black'},
                "basket": basket_weight,
            }
            if len(edge_reverse_dict) == 0:
                unique_edge = advocate_name + ' to ' + friend_name
                edge_reverse_dict[unique_edge] = edge_to_append
            else:
                # print(edge_reverse_dict)
                current_edge = advocate_name + ' to ' + friend_name
                if current_edge in [unique_edge for unique_edge in edge_reverse_dict]:
                    edge_reverse_dict[current_edge]['basket'] = str(float(edge_reverse_dict[current_edge]['basket']) + float(basket_weight))
                else:
                    edge_reverse_dict[current_edge] = edge_to_append
            
            data_to_display['edges'] = [v for k, v in edge_reverse_dict.items()]

        return data_to_display
    
    '''
    Following Centrality calculation functions uses Network X framework used to calculate centrality. 
    Mainly: nx.<centrality function>(Graph)
    '''
    def degree_centrality_topN(topN, G_symmetric):
        # Degree Centrality
        # print(G_symmetric)
        degCentrality = nx.degree_centrality(G_symmetric)
        degCentrality = {k: v for k, v in sorted(degCentrality.items(),reverse=True, key=lambda item: item[1])}
        degCentrality = dict(list(degCentrality.items())[:topN])
        degCentrality = json.dumps(degCentrality)
        # with open(BASE_DIR+ '/networkanalysis/static/js/degCentrality.json', 'w') as outfile:
        #     json.dump(degCentrality, outfile)
        return degCentrality
    def eigenvector_centrality_topN(topN, G_symmetric):
        # Eigenvector Centrality
        eigenCentrality = nx.eigenvector_centrality_numpy(G_symmetric)
        eigenCentrality = {k: v for k, v in sorted(eigenCentrality.items(),reverse=True, key=lambda item: item[1])}
        eigenCentrality = dict(list(eigenCentrality.items())[:topN])
        eigenCentrality = json.dumps(eigenCentrality)
        # with open(BASE_DIR+ '/networkanalysis/static/js/eigenCentrality.json', 'w') as outfile:
        #     json.dump(eigenCentrality, outfile)
        return eigenCentrality
    def betweenness_centrality_topN(topN, G_symmetric):
        # Betweeness Centrality
        betweennessCentrality = nx.betweenness_centrality(G_symmetric)
        betweennessCentrality = {k: v for k, v in sorted(betweennessCentrality.items(),reverse=True, key=lambda item: item[1])}
        betweennessCentrality = dict(list(betweennessCentrality.items())[:topN])
        # with open(BASE_DIR+ '/networkanalysis/static/js/betweennessCentrality.json', 'w') as outfile:
        #     json.dump(betweennessCentrality, outfile)
        betweennessCentrality = json.dumps(betweennessCentrality)
        return betweennessCentrality

    def convert_date_format(dateInputList):
        startDate = datetime.strptime(dateInputList[0], '%Y-%m-%d')
        endDate = datetime.strptime(dateInputList[1], '%Y-%m-%d')
        startDate = datetime.strftime(startDate, '%d %b %Y')
        endDate = datetime.strftime(endDate, '%d %b %Y')
        return [startDate, endDate]
        

    if "GET" == request.method:
        #  Dump to JSON format 
        data_to_calculate = load_data_to_display()
        data_to_display = json.dumps(load_data_to_display())
        # print('data to cal')
        # print(data_to_calculate)
        # if no data: nodes and edges empty
        if len(data_to_calculate['nodes']) == 0:
            return render(request, 'upload_csv.html', {"wrong_format_value_error": False, "order_number_missing": False, "csv_empty": True})

        # Execute analytcis
        G_symmetric = nx.Graph()
        for n in data_to_calculate["edges"]:
            G_symmetric.add_edge(n["from"], n["to"], weight=n["basket"])
        degCentrality = degree_centrality_topN(20, G_symmetric)
        eigenCentrality = eigenvector_centrality_topN(20, G_symmetric)
        betweennessCentrality = betweenness_centrality_topN(20, G_symmetric)

        return render(request, "analytics.html", {
            'degCentrality':degCentrality,
            'eigenCentrality':eigenCentrality,
            'betweennessCentrality':betweennessCentrality,
            'graphData':data_to_display,
            'startDate':'',
            'endDate':''
            })

        
    if "POST" == request.method:
        # from date filters
        dateInputList = request.POST.get('dateInput').split(',')
        dateInputFormatted = convert_date_format(dateInputList)
        
        data_to_calculate = load_data_to_display(dateInputList)
        data_to_display = json.dumps(load_data_to_display(dateInputList))
        # if len(data_to_calculate['nodes']) == 0:
        #     return render(request, 'upload_csv.html', {"wrong_format_value_error": False, "order_number_missing": False, "csv_empty": True})

        # if no nodes, means no edges, means no data, means return everything empty
        if len(data_to_calculate['nodes']) == 0:
            emptyDict = {}
            degCentrality = json.dumps(emptyDict)
            eigenCentrality = json.dumps(emptyDict)
            betweennessCentrality = json.dumps(emptyDict)
            
            return render(request, "analytics.html", {
                    'degCentrality':degCentrality,
                    'eigenCentrality':eigenCentrality,
                    'betweennessCentrality':betweennessCentrality,
                    'graphData':data_to_display,
                    'startDate':dateInputFormatted[0],
                    'endDate':dateInputFormatted[1]
                }) 

        # If data exists, Execute analytics
        else:
            G_symmetric = nx.Graph()
            for n in data_to_calculate["edges"]:
                G_symmetric.add_edge(n["from"], n["to"], weight=n["basket"])
            degCentrality = degree_centrality_topN(20,G_symmetric)
            eigenCentrality = eigenvector_centrality_topN(20,G_symmetric)
            betweennessCentrality = betweenness_centrality_topN(20,G_symmetric)
            
            return render(request, "analytics.html", {
                'degCentrality':degCentrality,
                'eigenCentrality':eigenCentrality,
                'betweennessCentrality':betweennessCentrality,
                'graphData':data_to_display,
                'startDate':dateInputFormatted[0],
                'endDate':dateInputFormatted[1]
                })


def clickDataQuery(request):
    ## Functions
    def append_to_csv(data):
        with open(data_export_file_path, 'a') as outfile:
            writer = csv.writer(outfile, delimiter = ',')
            for row in data:
                writer.writerow(row)
    
    def convert_query_to_csv(query_data):
        query_data = json.loads(query_data)
        data_to_csv = []
        for item in query_data:
            row_to_csv = []
            for key, value in item['fields'].items():
                row_to_csv.append(value)
            data_to_csv.append(row_to_csv)
        return data_to_csv

    def get_order_number_list():
        order_num_list = []
        with open(data_export_file_path, 'r') as infile:
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                print('row')
                print(row)
                if not row[0]:
                    return order_num_list
                order_num_list.append(row[8])
        return order_num_list

    def clean_data_query(order_num_list, query_data):
        # remove queries that are already existing witin the csv file 
        query_data = json.loads(query_data)
        data_to_csv = [item for item in query_data if item['fields']['Order_Number'] not in order_num_list]
        data_to_csv = json.dumps(data_to_csv)
        return data_to_csv
    
  
    if request.POST.get('node') == 'true':
        '''
         Note that for HTTPResponses for Ajax requests have to be in the django query format, which will be processed in renderGraph.js.
         Cleaning functions above check if order numbers already exist in the csv and only add unique orders transactions data. 
         This allows the user to select the same node multiple times but it will not export duplicate data.
        '''
        ## For Nodes
        if request.POST.get('start') == 'true':
            if request.POST.get('click', True):
                row_to_csv = ''
                data = request.POST.get('name')
                query_data = serializers.serialize('json', Referral.objects.filter(Advocate_Name=data[1:-1]) | Referral.objects.filter(Friend_Name=data[1:-1]))
                order_num_list = get_order_number_list()
                cleaned_query_data = clean_data_query(order_num_list, query_data)
                data_to_csv = convert_query_to_csv(cleaned_query_data)
                append_to_csv(data_to_csv)
                return HttpResponse(cleaned_query_data, content_type="application/json")
            elif request.POST.get('click', False):
                data = 'no click'
                return render(request, 'analytics.html', data)
        else:
            reset_csv() # clear the csv
            print('yeah resetting csv is called and action not started')
            if request.POST.get('click', True):
                data = request.POST.get('name')
                query_data = serializers.serialize('json', Referral.objects.filter(Advocate_Name=data[1:-1]) | Referral.objects.filter(Friend_Name=data[1:-1]))
                data_to_csv = convert_query_to_csv(query_data)
                append_to_csv(data_to_csv)
                return HttpResponse(query_data, content_type="application/json")
            elif request.POST.get('click', False):
                data = 'no click'
                return render(request, 'analytics.html', data)
    else:
        ## For Edges 
        if request.POST.get('start') == 'true':
            if request.POST.get('click', True):
                row_to_csv = ''
                data = request.POST.get('name')
                data = json.loads(data)
                query_data = serializers.serialize('json', Referral.objects.filter(Advocate_Name=data["from"]).filter(Friend_Name=data["to"]))
                order_num_list = get_order_number_list()
                cleaned_query_data = clean_data_query(order_num_list, query_data)
                data_to_csv = convert_query_to_csv(cleaned_query_data)
                append_to_csv(data_to_csv)
                return HttpResponse(cleaned_query_data, content_type="application/json")
            elif request.POST.get('click', False):
                data = 'no click'
                return render(request, 'analytics.html', data)
        else:
            reset_csv() # clear the csv
            print('yeah resetting csv is called and action not started')
            if request.POST.get('click', True):
                data = request.POST.get('name')
                data = json.loads(data)
                query_data = serializers.serialize('json', Referral.objects.filter(Advocate_Name=data["from"]).filter(Friend_Name=data["to"]))
                data_to_csv = convert_query_to_csv(query_data)
                append_to_csv(data_to_csv)
                return HttpResponse(query_data, content_type="application/json")
            elif request.POST.get('click', False):
                data = 'no click'
                return render(request, 'analytics.html', data)


def resetCSV(request):
    '''
    Click on white space to reset CSV with headers.
    ajax will fail but the important thing is to execute reset_csv() whenever the start/stop button is pressed.
    '''
    reset_csv()
    return HttpResponse('csv cleared', content_type="application/json")
    

