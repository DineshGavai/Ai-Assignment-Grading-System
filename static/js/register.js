function toggleFields() {
    const role = document.getElementById("role").value;
    document.getElementById("studentFields").style.display = role === "student" ? "grid" : "none";
    document.getElementById("teacherFields").style.display = role === "teacher" ? "grid" : "none";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("year").addEventListener("change", function () {
        let year = this.value;
        let semesterSelect = document.getElementById("semester");


        semesterSelect.innerHTML = '<option value="" disabled selected>Select Semester</option>';

        let semesters = [];


        if (year === "1st Year") {
            semesters = ["1", "2"];
        } else if (year === "2nd Year") {
            semesters = ["3", "4"];
        } else if (year === "3rd Year") {
            semesters = ["5", "6"];
        } else if (year === "4th Year") {
            semesters = ["7", "8"];
        }


        semesters.forEach(sem => {
            let option = document.createElement("option");
            option.value = sem;
            option.textContent = sem;
            semesterSelect.appendChild(option);
        });
    });
});
