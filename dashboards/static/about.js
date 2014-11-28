/**
 * Created by sukharni on 9/16/14.
 */



$("cont").innerHTML = "This management system is created and maintained by NCBI AppLog team."

//url = get_url()
//document.write('The url is: '+url +'<br />')
//document.write("The number of links is: "+ document.links.length)
//document.location.href = '/upload/'


//for(i=0; i<document.links.length; ++i){ //i below 0 for this page
  //  document.write("Link #"+ i+ " is: "+ document.links[i].href + '<br />')
//}

function get_url(){
    return document.documentURI

}
function $(id){
    return document.getElementById(id)
}