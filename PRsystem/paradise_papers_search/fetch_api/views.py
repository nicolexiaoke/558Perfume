from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views import View


from .utils import (
    count_nodes,
    fetch_nodes,
    fetch_ssnodes,
    fetch_sbnodes,
    fetch_spnodes,
    fetch_node_details,
    fetch_perfume_names,
    fetch_perfume_sizes,
)


class GetNodesCount(APIView):
    def get(self, request):
        count_info = {
            'node_type': request.GET.get('nodetype', ''),
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
            'node_type': request.GET.get('nodetype', ''),
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
        
        def myFunc_rating(e):
            return e['node_properties']['rating']
        def myFunc_price(e):
            return e['node_properties']['price']
        
        # if fetch_info['size'] == '':
        #     print('size is null')
        #     nodes.sort(key=myFunc_rating, reverse=True)
        # else:
        #     nodes.sort(key=myFunc_price, reverse=False)
        nodes.sort(key=myFunc_rating, reverse=True)
        
        print(nodes)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)

class GetLPNodesData(APIView):

    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('nodetype', ''),
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
        
        def myFunc_rating(e):
            return e['node_properties']['rating']
        def myFunc_price(e):
            return e['node_properties']['price']
        
        # if fetch_info['size'] == '':
        #     print('size is null')
        #     nodes.sort(key=myFunc_rating, reverse=True)
        # else:
        #     nodes.sort(key=myFunc_price, reverse=False)
        nodes.sort(key=myFunc_price, reverse=False)
        
        print(nodes)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)

class GetSSNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('nodetype', ''),
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

        nodes = fetch_ssnodes(fetch_info)
        print(nodes)

        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)

class GetSPNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('nodetype', ''),
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

        nodes = fetch_spnodes(fetch_info)
        print(nodes)

        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)


class GetSBNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('nodetype', ''),
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

        nodes = fetch_sbnodes(fetch_info)
        print(nodes)

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
        names = fetch_perfume_names()
        data = {
            'response': {
                'status': '200',
                'data': names,
            },
        }
        return Response(data)

class GetPerfumeSizes(APIView):
    def get(self, request):
        name_info = request.GET.get('pname', '')
        sizes = fetch_perfume_sizes(name_info)
        data = {
            'response': {
                'status': '200',
                'data': sizes,
            },
        }
        return Response(data)


class Index(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)


class RandomRecommendation(View):
    template = 'random_recommendation.html'

    def get(self, request):
        return render(request, self.template)

class SimilarRecommendation(View):
    template = 'similar_recommendation.html'

    def get(self, request):
        return render(request, self.template)


class PriceRecommendation(View):
    template = 'price_recommendation.html'

    def get(self, request):
        return render(request, self.template)
