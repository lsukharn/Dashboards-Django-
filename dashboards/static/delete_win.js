/**
 * Created by sukharni on 10/10/14.
 */
function newWindow() {
    var myWindow = window.open("", "_blank", "width=300, height=300");
    delete myWindow.document.attributes;
    myWindow.document.write("<script type=\"text/javascript\"> function closeWindow(){window.close();} \n"+
    "</script>");
    myWindow.document.write("<p>WARNING! You are about ot delete: " +
        $('dash_name').rows[1].cells.item(1).innerHTML +
    "</p>");
    myWindow.document.write("<table><tr><td>");
    myWindow.document.write("<p>" +
        "<button onclick=\"document.getElementById('dash_name').rows[1].cells.item(1).lastChild.value\">OK</button>" + "</p>");
    myWindow.document.write("</td>")
    myWindow.document.write("<td>")
    myWindow.document.write("<p><button onclick=\"closeWindow()\">Cancel</button>" + "</p>");
    myWindow.document.write("</td></tr></table>");
    /*window.open("http://www.google.com", "_blank", "width=300, height=300");*/
}
document.open("127.0.0.1:8000/logged")

function $(id){
    return document.getElementById(id);

}
