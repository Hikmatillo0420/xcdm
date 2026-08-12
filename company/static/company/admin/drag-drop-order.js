/* Django admin changelist'da qatorlarni sichqoncha bilan tortib tartiblash. */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    function getCookie(name) {
        var prefix = name + '=';
        var parts = (document.cookie || '').split(';');
        for (var i = 0; i < parts.length; i++) {
            var part = parts[i].trim();
            if (part.indexOf(prefix) === 0) {
                return decodeURIComponent(part.substring(prefix.length));
            }
        }
        return null;
    }

    function csrfToken() {
        var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return input ? input.value : getCookie('csrftoken');
    }

    onReady(function () {
        var handles = document.querySelectorAll('.drag-handle[data-reorder-url]');
        if (!handles.length) {
            return;
        }

        var firstRow = handles[0].closest('tr');
        if (!firstRow || !firstRow.parentNode) {
            return;
        }

        var tbody = firstRow.parentNode;
        var reorderUrl = handles[0].getAttribute('data-reorder-url');
        var dragged = null;
        var savedOrder = currentPks();

        function rows() {
            return Array.prototype.filter.call(tbody.rows, function (row) {
                return row.querySelector('.drag-handle') !== null;
            });
        }

        function currentPks() {
            return rows().map(function (row) {
                return row.querySelector('.drag-handle').getAttribute('data-pk');
            });
        }

        function restripe() {
            rows().forEach(function (row, index) {
                row.classList.remove('row1', 'row2');
                row.classList.add(index % 2 ? 'row2' : 'row1');
            });
        }

        function save() {
            var pks = currentPks();
            if (pks.join(',') === savedOrder.join(',')) {
                return;
            }

            tbody.classList.add('reorder-saving');
            fetch(reorderUrl, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({pks: pks})
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP ' + response.status);
                }
                return response.json();
            }).then(function (data) {
                savedOrder = data.pks;
                rows().forEach(function (row, index) {
                    row.querySelector('.drag-handle')
                        .setAttribute('data-order', data.positions[index]);
                });
                tbody.classList.remove('reorder-saving');
            }).catch(function (error) {
                tbody.classList.remove('reorder-saving');
                window.alert('Tartibni saqlab bo\'lmadi: ' + error.message);
                window.location.reload();
            });
        }

        rows().forEach(function (row) {
            var handle = row.querySelector('.drag-handle');

            // Qator faqat tutqichdan ushlanganda tortiladi — matn tanlash buzilmaydi.
            handle.addEventListener('mousedown', function () {
                row.setAttribute('draggable', 'true');
            });
            handle.addEventListener('mouseup', function () {
                row.removeAttribute('draggable');
            });

            row.addEventListener('dragstart', function (event) {
                dragged = row;
                row.classList.add('drag-source');
                event.dataTransfer.effectAllowed = 'move';
                // Firefox dataTransfer bo'sh bo'lsa tortishni boshlamaydi.
                event.dataTransfer.setData('text/plain', '');
            });

            row.addEventListener('dragend', function () {
                row.removeAttribute('draggable');
                row.classList.remove('drag-source');
                dragged = null;
                restripe();
                save();
            });

            row.addEventListener('dragover', function (event) {
                if (!dragged || dragged === row) {
                    return;
                }
                event.preventDefault();
                event.dataTransfer.dropEffect = 'move';

                var box = row.getBoundingClientRect();
                if (event.clientY - box.top > box.height / 2) {
                    if (row.nextSibling !== dragged) {
                        tbody.insertBefore(dragged, row.nextSibling);
                    }
                } else if (row.previousSibling !== dragged) {
                    tbody.insertBefore(dragged, row);
                }
            });

            row.addEventListener('drop', function (event) {
                event.preventDefault();
            });
        });
    });
})();
