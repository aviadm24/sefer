
function setStorage(objectName, myObject){
    if(!sessionStorage[objectName]){
        sessionStorage.setItem(objectName, myObject);
    }
}


function getStorage(objectName){
    if(sessionStorage[objectName]){
        var myObject = sessionStorage.getItem(objectName);
    }
    return myObject;
}
