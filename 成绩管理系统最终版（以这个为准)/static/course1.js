async function renderList() {
    let response = await fetch(`/api/course/list`);
    if (!response.ok) {
        console.error(response);
        return;
    }

    let data = await response.json();

    let tbodyEl = document.createElement("tbody");
    for (let item of data) {
        let trEl = document.createElement("tr");
        tbodyEl.append(trEl);

        let tdEl;
        tdEl = document.createElement("td");
        tdEl.innerText = item.sch_term;
        tdEl.className = "sch_term";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "cou_plan_name";
        tdEl.innerText = item.cou_plan_name;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "cou_plan_time";
        tdEl.innerText = item.cou_plan_time;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "cou_plan_place";
        tdEl.innerText = item.cou_plan_place;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "ctrlbar";
        tdEl.append(renderRecordCtrlbar(item));
        trEl.append(tdEl);
    }

    let tableEl = document.querySelector("#course-table");
    document.querySelector("#course-table > tbody").remove();
    tableEl.append(tbodyEl);
}

function renderRecordCtrlbar(item) {
    let ctrlbarEl = document.createElement("div");

    let editBtn = document.createElement("a");
    editBtn.className = "btn";
    editBtn.innerText = "修改";
    editBtn.onclick = (e) => {
        openEditDialog(item);
    };
    ctrlbarEl.append(editBtn);

    let delBtn = document.createElement("a");
    delBtn.className = "btn";
    delBtn.innerText = "删除";
    delBtn.onclick = (e) => {
        openComfirmationDialog({
            message: `确定要删除这个课程计划？`,
            onOk: () => {
                (async () => {
                    let response = await fetch(`/api/course/${item.cou_plan_sn}/${item.sch_term}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) {
                        console.error(response);
                    }

                    renderList();
                })();
            },
        });
    };
    ctrlbarEl.append(delBtn);

    return ctrlbarEl;
}

async function openEditDialog(item) {
    let dialog = document.querySelector(".course-editor");

    let dialogTitle = dialog.querySelector(".dialog-head");
    let form = dialog.querySelector("form");

    if (item) {
        dialogTitle.innerText = `修改教学计划 (#${item.cou_plan_sn})`;     
        form.elements.cou_plan_sn.value = item.cou_plan_sn ?? null;
        form.elements.sch_term.value = item.sch_term ?? "";
        form.elements.cou_plan_name.value = item.cou_plan_name ?? "";
        form.elements.cou_plan_time.value = item.cou_plan_time ?? "";
        form.elements.cou_plan_place.value = item.cou_plan_place ?? "";
    } else {
        dialogTitle.innerText = "新建教学计划";
        form.elements.cou_plan_sn.value = null;
        form.elements.sch_term.value = "";
        form.elements.cou_plan_name.value = "";
        form.elements.cou_plan_time.value = "";
        form.elements.cou_plan_place.value = "";
    }

    if (dialog.classList.contains("open")) {
        dialog.classList.remove("open");
    } else {
        dialog.classList.add("open");
    }
}

async function renderEditDialog() {
    let newStudentBtn = document.querySelector(".paper #new-btn");
    newStudentBtn.onclick = (e) => {
        openEditDialog();
    };

    let dialog = document.querySelector(".course-editor");

    let form = dialog.querySelector("form");

    let close_btn = dialog.querySelector("#close-btn");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    close_btn.onclick = closeDialog;

    let save_btn = dialog.querySelector("#save-btn");
    save_btn.onclick = (e) => {
        let data = {
            cou_plan_sn: form.elements.cou_plan_sn.value,
            sch_term: form.elements.sch_term.value,
            cou_plan_name: form.elements.cou_plan_name.value,
            cou_plan_time: form.elements.cou_plan_time.value,
            cou_plan_place: form.elements.cou_plan_place.value,
        };

        if (!data.cou_plan_sn) {
            // 异步执行POST请求操作
            (async () => {
                let response = await fetch("/api/course", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        } else {
            // 异步执行PUT请求操作
            (async () => {
                let response = await fetch(`/api/course/${data.cou_plan_sn}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        }
    };
}

async function openComfirmationDialog({ message, onOk, onCancel }) {
    let dialog = document.querySelector(".comfirmation-dialog");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    let okBtn = dialog.querySelector("#ok-btn");
    okBtn.onclick = (e) => {
        if (typeof onOk === "function") {
            onOk();
        }

        closeDialog();
    };

    let cancelBtn = dialog.querySelector("#cancel-btn");
    cancelBtn.onclick = (e) => {
        if (typeof onCancel === "function") {
            onCancel();
        }

        closeDialog();
    };

    let messageEl = dialog.querySelector("#message");
    messageEl.innerText = message;

    dialog.classList.add("open");
}

document.addEventListener("DOMContentLoaded", (e) => {
    renderList();
    renderEditDialog();
});
