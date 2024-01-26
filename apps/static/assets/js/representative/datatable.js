var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
        { orderable: false, targets: [3,4,6,7] },
        { searchable: false, targets: [0] }
    ],
    pageLength: 10,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listrepresentative();

    dataTable = $("#datatable-apoderado").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listrepresentative = async () => {

    try {
        // const response = await fetch("https://ee68-200-104-216-49.ngrok-free.app/representative/list_representative/"); //Tener en cuenta siempre el link
        const response = await fetch("http://127.0.0.1:9999/representative/list_representative/");
        const data = await response.json();

        console.log(response)

        let content = ``;
        data.representatives.forEach((representative, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${representative.name}</td>
                    <td>${representative.last_name}</td>
                    <td>${representative.email}</td>
                    <td>${representative.phone}</td>
                    <td>${representative.email}</td>
                    <td>
                        <a href="${representative.edit_url}">
                            <button class='btn btn-sm btn-primary'><span class="material-icons">edit</span></button>
                        </a>
                    </td>
                    <td>
                        <a href="${representative.delete_url}">
                            <button class='btn btn-sm btn-danger'><span class="material-icons">delete</span></button>
                        </a>
                    </td>
                </tr>`;
        });
        tableBody_apoderado.innerHTML = content;

    } catch (ex) {
        alert(ex);
        alert('Error de response');
    }

};

window.addEventListener("load", async () => {
    await initDataTable();
});

// {/* <td>${representative.score >= 8
//                         ? "<i class='fa-solid fa-check' style='color: green;'></i>"
//                         : "<i class='fa-solid fa-xmark' style='color: red;'></i>"}
//                     </td> */}