(function(Vue, api) {
  window.indexComponent = new Vue({
    el: '#index',
    delimiters: ['${', '}'],
    data: {
      size: undefined,
      finish: undefined,
      type: undefined,
      sizes: [],
      types: [],
      finishes: [],
      widgets: [],
    },
    created: function() {
      this.getWidgets();
      this.getWidgetSizes();
      this.getWidgetFinishes();
      this.getWidgetTypes();
    },
    methods: {
      getWidgets: function() {
        var self = this;
        var params = {
          size: this.size,
          type: this.type,
          finish: this.finish,
        };

        api.fetchWidgets(params).then(function(response) {
          self.widgets = response.data;
        })
      },
      getWidgetSizes: function() {
        var self = this;

        api.fetchWidgetSizes().then(function(response) {
          self.sizes = response.data;
        });
      },
      getWidgetFinishes: function() {
        var self = this;

        api.fetchWidgetFinishes().then(function(response) {
          self.finishes = response.data;
        });
      },
      getWidgetTypes: function() {
        var self = this;

        api.fetchWidgetTypes().then(function(response) {
          self.types = response.data;
        });
      },
      changeSize: function(event) {
        this.size = event.target.value;
        this.getWidgets();
      },
      changeFinish: function(event) {
        this.finish = event.target.value;
        this.getWidgets();
      },
      changeType: function(event) {
        this.type = event.target.value;
        this.getWidgets();
      },
    }
  })
})(Vue, window.api);