(function() {
  // Your web app's Firebase configuration

  console.log("Loading firebase.");

  var config = {
      apiKey: "AIzaSyDGD8ewVOBVxl6O1r35Npy2RRw2dlWGdP8",
      authDomain: "mapuavitalsignsdatabase.firebaseapp.com",
      databaseURL: "https://mapuavitalsignsdatabase.firebaseio.com",
      projectId: "mapuavitalsignsdatabase",
      storageBucket: "mapuavitalsignsdatabase.appspot.com",
      messagingSenderId: "582213066054",
      appId: "1:582213066054:web:ab72ca16bf4849166bd947",
      measurementId: "G-G5FC6W67QF",

  }

  // Initialize Firebase
  firebase.initializeApp(config);

  console.log("Firebase loaded.")

  var rootRef = firebase.database().ref();
  var urlRef = rootRef.child("users");

  urlRef.on('value', function(snapshot) {
    console.log("debug")
    console.log(snapshot)

  });




}());
