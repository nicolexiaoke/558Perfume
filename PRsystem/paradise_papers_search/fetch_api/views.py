from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .utils import (
    count_nodes,
    fetch_nodes,
    fetch_node_details,
    fetch_perfume_names
)


class GetNodesCount(APIView):
    def get(self, request):
        count_info = {
            'node_type': request.GET.get('nodetype', 'Perfume'),
            'name': request.GET.get('nodename', ''),
            'size': request.GET.get('nodesize', ''),
            'smell': request.GET.get('nodesmell', ''),
            'lprice': float(request.GET.get('nodelprice', 0)),
            'hprice': float(request.GET.get('nodehprice', 100000000)),
            'lrating': float(request.GET.get('nodelrating', 5)),
            'hrating': float(request.GET.get('nodehrating', 0)),
        }
        count = count_nodes(count_info)
        data = {
            'response': {
                'status': '200',
                'data': count,
            },
        }
        return Response(data)


class GetNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('nodetype', 'Perfume'),
            'name': request.GET.get('nodename', ''),
            'size': request.GET.get('nodesize', ''),
            'smell': request.GET.get('nodesmell', ''),
            'lprice': float(request.GET.get('nodelprice', 0)),
            'hprice': float(request.GET.get('nodehprice', 100000000)),
            'lrating': float(request.GET.get('nodelrating', 5)),
            'hrating': float(request.GET.get('nodehrating', 0)),
            'limit': 10,
            'page': int(request.GET.get('p', 1)),
        }
        nodes = fetch_nodes(fetch_info)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)
    

'''buggy! ID of nodes not solved'''
class GetNodeData(APIView):
    def get(self, request):
        node_info = {
            'node_type': request.GET.get('nodetype', 'DeliveryOption'),
            'node_id': int(request.GET.get('nodeid')),
        }
        node_details = fetch_node_details(node_info)
        data = {
            'response': {
                'status': '200',
                'data': node_details,
            },
        }
        return Response(data)


class GetPerfumeNames(APIView):
    def get(self, request):
        countries = fetch_perfume_names()
        data = {
            'response': {
                'status': '200',
                'data': countries,
            },
        }
        return Response(data)

