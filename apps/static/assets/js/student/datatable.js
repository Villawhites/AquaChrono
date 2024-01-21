var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [3,4] },
        { searchable: false, targets: [0] }
    ],
    pageLength: 10,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await liststudent();

    dataTable = $("#datatable-alumnos").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const liststudent = async () => {

    try {
        // const response = await fetch("https://ee68-200-104-216-49.ngrok-free.app/student/list_student/"); //Tener en cuenta siempre el link
        const response = await fetch("http://127.0.0.1:9999/student/list_student/");
        console.log(response+'r')
        const data = await response.json();

        console.log(response)

        let content = ``;
        data.students.forEach((student, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${student.name}</td>
                    <td>${student.rut}</td>
                    <td>${student.birth_date}</td>
                    <td>
                        <a href="${student.edit_url}">
                            <button class='btn btn-sm btn-primary'><span class="material-icons">edit</span></button>
                        </a>
                    </td>
                    <td>
                        <a href="${student.delete_url}">
                            <button class='btn btn-sm btn-danger'><span class="material-icons">delete</span></button>
                        </a>
                    </td>
                </tr>`;
        });
        tableBody_alumnos.innerHTML = content;

    } catch (ex) {
        alert(ex);
        alert('Error de response');
    }

};

window.addEventListener("load", async () => {
    await initDataTable();
});

// {/* <td>${student.score >= 8
//                         ? "<i class='fa-solid fa-check' style='color: green;'></i>"
//                         : "<i class='fa-solid fa-xmark' style='color: red;'></i>"}
//                     </td> */}