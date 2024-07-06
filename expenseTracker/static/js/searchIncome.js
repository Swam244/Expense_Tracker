const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appOutput = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");

tableOutput.style.display = "none";

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    if(searchValue.trim().length > 0){
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        console.log(searchValue)
        fetch("/income/search-income",{
            body: JSON.stringify({searchText : searchValue}),
            method : "POST",
        }).then((res)=>res.json()).then((data)=>{
            tableOutput.style.display = "block";
            appOutput.style.display = "none";
            console.log(data);
            if(data.length === 0){
                noResults.style.display = "block";
                tableOutput.style.display="none";
            }
            else{
                noResults.style.display = "none";
                data.forEach((element) => {
                    tbody.innerHTML += `
                    <tr>
                    <td>${element.amount}</td>
                    <td>${element.source}</td>
                    <td>${element.date}</td>
                    <td>${element.description}</td>
                    </tr>
                    `
                });
            }
        })
    }
    else{
        tableOutput.style.display = "none";
        paginationContainer.style.display = "block";
        appOutput.style.display = "block";
    }
});