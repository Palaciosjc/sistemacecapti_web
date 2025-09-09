document.addEventListener('DOMContentLoaded', function() {
    const courseLinks = document.querySelectorAll('.course-link');
    const studentsTable = document.getElementById('students-table-body');
    const studentsTitle = document.getElementById('students-title');
    const studentsSection = document.getElementById('students-section');

    courseLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const courseId = this.dataset.courseId;
            fetch(`/course/${courseId}/students`)
                .then(res => res.json())
                .then(data => {
                    studentsTitle.textContent = this.textContent;
                    studentsTable.innerHTML = '';
                    if (data.length === 0) {
                        studentsTable.innerHTML = '<tr><td colspan="3">No hay alumnos inscritos.</td></tr>';
                    } else {
                        data.forEach(alumno => {
                            studentsTable.innerHTML += `
                                <tr>
                                    <td>${alumno.nombre}</td>
                                    <td>
                                        <input type="number" min="0" max="20" step="0.1" value="${alumno.calificacion !== null ? alumno.calificacion : ''}" class="form-control form-control-sm grade-input" data-insc-id="${alumno.id_inscripcion}">
                                    </td>
                                    <td>
                                        <button class="btn btn-sm btn-success save-grade" data-insc-id="${alumno.id_inscripcion}">Guardar</button>
                                    </td>
                                </tr>
                            `;
                        });
                    }
                    studentsSection.style.display = 'block';
                });
        });
    });

    // Delegación para guardar calificación
    studentsTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('save-grade')) {
            const inscId = e.target.dataset.inscId;
            const input = document.querySelector(`input.grade-input[data-insc-id='${inscId}']`);
            const grade = parseFloat(input.value);
            fetch(`/inscription/${inscId}/grade`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ grade })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                } else {
                    input.classList.remove('is-valid');
                    input.classList.add('is-invalid');
                    alert(data.error || 'Error al guardar la calificación');
                }
            });
        }
    });
});
