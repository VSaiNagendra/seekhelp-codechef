var params = (new URL(document.location)).searchParams;
var name = params.get("code");
requestToken();
var xhttp1,xhttp2;
function requestToken() {
  
  xhttp1 = new XMLHttpRequest();
  xhttp1.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log('request is success');
     console.log(JSON.parse(xhttp1.responseText).result.data.access_token);
     xhttp2=new XMLHttpRequest();
     xhttp2.open("GET", "https://api.codechef.com/contests/PRACTICE/problems/SALARY", false);
 	 xhttp2.setRequestHeader("content-type", "application/json");
 	 xhttp2.setRequestHeader("authorization", "Bearer "+JSON.parse(xhttp1.responseText).result.data.access_token.toString());
 	 xhttp2.send();
    }
  };
  xhttp1.open("POST", "https://api.codechef.com/oauth/token", false);
  xhttp1.setRequestHeader("content-type", "application/json");
  xhttp1.send(JSON.stringify({"grant_type":"authorization_code","code":name.toString(),"client_id":"a420ca7d74ada05e8b29411205403ca4","client_secret":"ab9b1e3c02b7bb2f98080f26372b16f6","redirect_uri":"http://149.129.138.34/"}))
}