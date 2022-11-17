/**
 * Paradise Paper Search App
 *
 * @author: Junior Báez
 * @version: 0.2.0
 * @requires ko - global KnowckoutJS object
 *
 * @todo Implement RequireJS and split app into modules
 * @todo Implement page routing, possibly with Page.js
 * @todo Write JSDocs
 *
 */
(() => {
  'use strict';

  /**
  *  Nodes Settings metadata
  *  {
  *    '<node_type>': {
  *        '<property_name>': ['<Property Label>', <boolDisplayTable>],
  *        ...
  *    },
  *   ...
  *  }
  *
  * @todo Add missing properties
  */


  const nodes_settings = {
    'Perfume': {
      'name': ['name', true],
      'size': ['size', true],
      'price': ['price', true],
      'rating': ['rating', true],
      'url': ['url', true]
    }
  };

  /**
   * Representation of a Node
   *
   * @param node_type
   * @param node_properties
   */
  class Node {

    constructor(node_type, node_id_or_properties) {
      this._node_type = node_type;
      this._node_properties = {};
      this._node_connections = ko.observableArray();
      this._fetchStateNode = ko.observable(false);

      if (typeof node_id_or_properties === 'number') {
        this._node_id = node_id_or_properties;
      } else {
        this._node_id = node_id_or_properties.node_id;
        this._node_properties = node_id_or_properties;
      }
    }

    /**
     * Fetch connected nodes.
     */
    fetchConnections () {
      this._fetchStateNode(true);
      $.getJSON(
        '/fetch/node',
        {
          'id': this._node_id,
          'nodetype': this._node_type
        }
      )
      .done(nodeFetch => {
        this._node_properties = nodeFetch.response.data.node_properties;
        nodeFetch.response.data.node_connections.forEach(conns => {
          conns.nodes_count = conns.nodes_related.length;
          // check if the current connections group really has nodes
          if (conns.nodes_count > 0) {
            // Convert nodes_related to instaces of the class Node
            conns.nodes_related = conns.nodes_related.map((n) => {
              return new Node(conns.nodes_type, n.node_properties);
            });
            this._node_connections.push(conns);
          }
        });
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchStateNode(false);
      });
    }
  }

  /**
   * The purpose of this class is to fetch data.
   * Each instance of the class will search and filter a specific node type.
   *
   * @param node_type
   * @param node_settings
   */
  class NodeSearch {

    constructor(node_type, node_settings) {
      /**
       * Type of Nodes to fetch
       */
      this._node_type = node_type;

      /**
       * List of node properties metadata
       *
       * [
       *  {
       *    property_name: <propertyname>,
       *    property_label: <Property Label>
       *    property_display_table: <bool>
       *  },
       *  ...
       * ]
       */
      this._nodePropertyList = [];

      /**
       * Container of Nodes
       * as an observableArray in order to dynamicly update the view
       */
      this._nodeSearchData = ko.observableArray();

      /**
       * How many nodes have being fetched
       */
      this._nodeSearchDataCount = ko.observable(-1);

      /**
       * Show related tab on the view.
       */
      this._activateTab = ko.observable(false);

      /**
       * State of the current fetch
       */
      this._fetchState = ko.observable(false);

      /**
       * API endpoint
       */
      this._search_api = '/fetch/';

      /**
       * Filter the Nodes that will be fetched
       */
      this._search_filters = {
        'nodetype': this._node_type,
      };

      /**
       * Last page fetched
       */
      this._last_page_fetched = ko.observable(0);

      // Construct _nodePropertyList defined above
      for (let property_name in node_settings) {
        // console.log('-------------')
        if (node_settings.hasOwnProperty(property_name)) {
          // console.log('****************')
          // console.log(property_name, node_settings[property_name])
          
          this._nodePropertyList.push({
            property_name,
            'property_label': node_settings[property_name][0],
            'property_display_table': node_settings[property_name][1]
          });
        }
      }
      console.log('this._nodePropertyList:',this._nodePropertyList)
    }

   /**
    * Set the filters
    *
    * @param: newFilters - Object of filters to change
    * @return: this._search_filters
    */
    setFilters(newFilters) {
      return Object.assign(this._search_filters, newFilters);
    }

    fetch () {
      this._fetchState(true);

      $.getJSON(
        this._search_api + 'nodes',
        this.setFilters({ 'p': this._last_page_fetched() + 1 })
      )
      .done(nodes => {
        nodes.response.data.forEach(node => {
          this._nodeSearchData.push(
            new Node(this._node_type, node.node_properties)
          );
        });
        this._last_page_fetched(this._last_page_fetched() + 1);
        console.log('in Nodesearch.fetch, this._nodeSearchData', this._nodeSearchData())
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchState(false);
      });
    }

    lowest_price_fetch () {
      this._fetchState(true);

      $.getJSON(
        this._search_api + 'lpnodes',
        this.setFilters({ 'p': this._last_page_fetched() + 1 })
      )
      .done(nodes => {
        nodes.response.data.forEach(node => {
          this._nodeSearchData.push(
            new Node(this._node_type, node.node_properties)
          );
        });
        this._last_page_fetched(this._last_page_fetched() + 1);
        console.log('in Nodesearch.lowest_price_fetch, this._nodeSearchData', this._nodeSearchData())
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchState(false);
      });
    }

    similar_scent_fetch () {
      this._fetchState(true);

      $.getJSON(
        this._search_api + 'ssnodes',
        this.setFilters({ 'p': this._last_page_fetched() + 1 })
      )
      .done(nodes => {
        nodes.response.data.forEach(node => {
          this._nodeSearchData.push(
            new Node(this._node_type, node.node_properties)
          );
        });
        this._last_page_fetched(this._last_page_fetched() + 1);
        console.log('in Nodesearch.similar_scent_fetch, this._nodeSearchData', this._nodeSearchData())
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchState(false);
      });
    }

    similar_price_fetch () {
      this._fetchState(true);

      $.getJSON(
        this._search_api + 'spnodes',
        this.setFilters({ 'p': this._last_page_fetched() + 1 })
      )
      .done(nodes => {
        nodes.response.data.forEach(node => {
          this._nodeSearchData.push(
            new Node(this._node_type, node.node_properties)
          );
        });
        this._last_page_fetched(this._last_page_fetched() + 1);
        console.log('in Nodesearch.similar_scent_fetch, this._nodeSearchData', this._nodeSearchData())
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchState(false);
      });
    }

    same_brand_fetch () {
      this._fetchState(true);

      $.getJSON(
        this._search_api + 'sbnodes',
        this.setFilters({ 'p': this._last_page_fetched() + 1 })
      )
      .done(nodes => {
        nodes.response.data.forEach(node => {
          this._nodeSearchData.push(
            new Node(this._node_type, node.node_properties)
          );
        });
        this._last_page_fetched(this._last_page_fetched() + 1);
        console.log('in Nodesearch.same_brand_fetch, this._nodeSearchData', this._nodeSearchData())
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
      .always(() => {
        this._fetchState(false);
      });
    }

    fetchCount() {
      console.log('in fetchCount')
      console.log(this._search_filters)
      $.getJSON(
        this._search_api + 'count',
        this._search_filters
      )
      .done(nodes => {
        this._nodeSearchDataCount(nodes.response.data.count)
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
    }

    /**
     * Clear and reset 
     */
    clear () {
      this._nodeSearchData([]);
      this._last_page_fetched(0);
      this._nodeSearchDataCount(-1);
      this.setFilters({
          'q': '',
          'c': '',
          'nodename': '',
          'p': 0,
      });
    }

  }

  /**
   * This is the actual ModelView app
   *
   */
  class SearchApp {

    constructor() {
      this._initialSearchDone = ko.observable(false);
      this._inLowestPriceState = ko.observable(false);
      this._inSimilarScentState = ko.observable(false);
      this._inSimilarPriceState = ko.observable(false);
      this._inSameBrandState = ko.observable(false);
      this._searchText = ko.observable('');
      this._countryList = ko.observableArray();
      this._perfumeNameList = ko.observableArray();
      this._perfumeSizeList = ko.observableArray();
      this._filters = {};

      // Node details tracking
      this._nodesCache = {};
      this._currentNode = ko.observable();

      // Construct NodeSearch instances
      this._nodeSearch = {};
      this._nodeSearchList = ko.observableArray([]);
      for (let node_type in nodes_settings) {
        if (nodes_settings.hasOwnProperty(node_type)) {
          const nodeSearch = new NodeSearch(node_type, nodes_settings[node_type]);
          this._nodeSearch[node_type] = nodeSearch;
          this._nodeSearchList.push(nodeSearch);
        }
        console.log('this._nodeSearchList:')
        console.log(this._nodeSearchList()[0])
      }

      this._currentNodeSearch = this._nodeSearchList()[0];
      this.fetchCountries();
      this.fetchPerfumeNames();
      // this.fetchPerfumeSizes();
    }

    /**
     * Init Search
     */
    initNodeSeach () {
      console.log("into initNodeSearch")
      console.log('inLowestPriceState:', this._inLowestPriceState());
      console.log('inSimilarScentState:', this._inSimilarScentState());

      this._nodeSearchList().forEach(nodeSearch => {
        
        console.log("into nodesearchlist")

        nodeSearch.clear();
        nodeSearch.setFilters({
          'q': this._searchText(),
          'c': this._filters['country'],
          'nodename': this._filters['perfume_names'],
          'nodesize': this._filters['perfume_sizes'],
        });

        nodeSearch.fetchCount();
      });
      console.log("outof nodesearchlist")

      this._initialSearchDone(true)
      console.log("_initialSearchDone:", this._initialSearchDone())
      this.displayNodeSearch();
      
      /* reset states*/
      this._inLowestPriceState(false);
      this._inSimilarScentState(false);
      this._inSimilarPriceState(false);
      this._inSameBrandState(false);
    }

    setLowestPriceState(){
      console.log('setLowestPriceState');
      console.log('inLowestPriceState:', this._inLowestPriceState());
      this._inLowestPriceState(true);
      console.log('inLowestPriceState:', this._inLowestPriceState());
    }
    setSimilarScentState(){
      console.log('setSimilarScentState');
      console.log('setSimilarScentState:', this._inSimilarScentState());
      this._inSimilarScentState(true);
      console.log('inLowestPriceState:', this._inSimilarScentState());
    }
    setSimilarPriceState(){
      console.log('setSimilarPriceState');
      console.log('setSimilarPriceState:', this._inSimilarPriceState());
      this._inSimilarPriceState(true);
      console.log('setSimilarPriceState:', this._inSimilarPriceState());
    }
    setSameBrandState(){
      console.log('setSameBrandState');
      console.log('setSameBrandState:', this._inSameBrandState());
      this._inSameBrandState(true);
      console.log('setSameBrandState:', this._inSameBrandState());
    }

    /**
     * Toggle _currentNodeSearch to show on the view
     */
    displayNodeSearch (nodeSearch) {
      console.log('in displayNodeSearch')
      console.log('nodeSearch:', nodeSearch)
      
      if (nodeSearch) {
        console.log('displayNodeSearch: into if')
        this._currentNodeSearch._activateTab(false);
        this._currentNodeSearch = nodeSearch;
      }

      this._currentNodeSearch._activateTab(true);

      console.log("_last_page_fetched():", this._currentNodeSearch._last_page_fetched())
      if (this._currentNodeSearch._last_page_fetched() === 0) {
        if (this._inLowestPriceState()){
          this._currentNodeSearch.lowest_price_fetch();
        }
        else if(this._inSimilarScentState()){
          this._currentNodeSearch.similar_scent_fetch();
        }
        else if(this._inSameBrandState()){
          this._currentNodeSearch.same_brand_fetch();
        }
        else if(this._inSimilarPriceState()){
          this._currentNodeSearch.similar_price_fetch();
        }
        else{
          this._currentNodeSearch.fetch();
        }

      }
    }

    /**
     * Toggle _currentNode to show on the view
     */
    displayNode (node) {
      const url = node._node_properties.url;
      window.open(url);


      // const node_id = node._node_id;
      // // Show node from cache if connections have being fetched
      // if (this._nodesCache.hasOwnProperty(node_id)) {
      //   this._currentNode(this._nodesCache[node_id]);
      //   return;
      // }

      // // Fetch node connections once
      // node.fetchConnections();
      // this._currentNode(node);
      // this._nodesCache[node_id] = node;
    }
    
    sortByAttr (attr) {
      console.log('in sortByAttr');
      console.log(attr);

    }

    fetchCountries() {
      // $.getJSON(
      //   'fetch/countries'
      // )
      // .done(countries => {
      //   countries.response.data.forEach(country => {
      //     this._countryList.push(country);
      //   });
      // })
      // .fail(() => {
      //   /** @todo Handle errors */
      //   console.log("Fetch error");
      // })
    }

    fetchPerfumeNames() {
      $.getJSON(
        'fetch/perfume_names'
      )
      .done(perfume_names => {
        perfume_names.response.data.forEach(perfume_name => {
          this._perfumeNameList.push(perfume_name);
          console.log("done");
        });
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
        console.log("done");
      })
    }

    fetchPerfumeSizes() {
      this._perfumeSizeList.removeAll();
      $.getJSON(
        'fetch/perfume_sizes',
        {
          'pname': this._filters['perfume_names'],
        }
      )
      .done(perfume_sizes => {
        perfume_sizes.response.data.forEach(perfume_size => {
          this._perfumeSizeList.push(perfume_size);
        });
      })
      .fail(() => {
        /** @todo Handle errors */
        console.log("Fetch error");
      })
    }
  }

  // Create and bind our SearchApp
  ko.applyBindings(new SearchApp());
})();
