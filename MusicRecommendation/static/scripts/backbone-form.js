$(function(){
  var User = Backbone.Model.extend({
      defaults: {
        birthyear
        bikeid
        gender
        startstationid
        startstationname
        startstationlatitude
        startstationlongitude
        endstationid
        endstationname
        endstationlatitude
        endstationlongitude
        starttime
        stoptime
        tripduration: "Not specified"
      },
      initialize: function(){
        console.log("Music is the answer");
      }
  });
  var UserList = Backbone.Collection.extend({
    model: User
  });
  //  Users View
  var UsersView = Backbone.View.extend({
    template: _.template($('#trip_template').html()),
    render: function(event){
      _.each(this.model.models, function(user){
        var username = user.attributes['username'];
        var email = user.attributes['email'];

        //  Assign template
        var template = this.template(user.toJSON());

        $(this.el).append(template);
      }, this);
      return this;
    }
  });

  var user = new User({

  });

  var userList = new UserList;

  //  Application View
  var AppView = Backbone.View.extend({
    el: 'body',
    render: function(){
      var usersView = new UsersView({model:userList});
      var usersViewRender = usersView.render().el;
      $('.users').html(usersViewRender);
    },
    initialize: function(){
      var Options = {};
      Options.success = this.render;
      userList.fetch(Options);
    }
  });

  var App = new AppView;
});