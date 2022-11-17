from django.conf.urls import url

from .views import (
    GetNodesCount,
    GetNodesData,
    GetNodeData,
    GetPerfumeNames,
    GetPerfumeSizes, 
    GetLPNodesData,
    GetSSNodesData,
    GetSBNodesData,
    GetSPNodesData
)


urlpatterns = [
    url(r'^count[/]?$', GetNodesCount.as_view(), name='get_nodes_count'),
    url(r'^nodes[/]?$', GetNodesData.as_view(), name='get_nodes_data'),
    url(r'^lpnodes[/]?$', GetLPNodesData.as_view(), name='get_lpnodes_data'),
    url(r'^ssnodes[/]?$', GetSSNodesData.as_view(), name='get_ssnodes_data'),
    url(r'^sbnodes[/]?$', GetSBNodesData.as_view(), name='get_sbnodes_data'),
    url(r'^spnodes[/]?$', GetSPNodesData.as_view(), name='get_spnodes_data'),
    url(r'^node[/]?$', GetNodeData.as_view(), name='get_node_data'),
    url(r'^perfume_names[/]?$', GetPerfumeNames.as_view(), name='get_perfume_names'),
    url(r'^perfume_sizes[/]?$', GetPerfumeSizes.as_view(), name='get_perfume_sizes'),
]

