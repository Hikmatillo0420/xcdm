/* Django admin changelist: qatorni ushlab tortish orqali tartiblash. */
(function () {
    'use strict';

    var INTERACTIVE = 'a, button, input, select, textarea, label, .related-widget-wrapper';

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

    /* Qatordagi obyekt id'si: avval action checkbox, bo'lmasa tahrirlash havolasi. */
    function rowPk(row) {
        var checkbox = row.querySelector('input[name="_selected_action"]');
        if (checkbox && checkbox.value) {
            return checkbox.value;
        }
        var links = row.querySelectorAll('a[href]');
        for (var i = 0; i < links.length; i++) {
            var match = links[i].getAttribute('href').match(/([^/]+)\/change\/?(?:\?|$)/);
            if (match) {
                return decodeURIComponent(match[1]);
            }
        }
        return null;
    }

    onReady(function () {
        // Ro'yxat boshqa ustun bo'yicha saralangan yoki qidiruv ishlatilgan
        // bo'lsa, tortish mantiqsiz — o'chirib qo'yamiz.
        if (/[?&](o|q)=/.test(window.location.search)) {
            return;
        }

        var table = document.getElementById('result_list');
        if (!table || !table.tBodies.length) {
            return;
        }

        var tbody = table.tBodies[0];
        var reorderUrl = window.location.pathname.replace(/\/?$/, '/') + 'reorder/';
        var dragged = null;

        function rows() {
            return Array.prototype.filter.call(tbody.rows, function (row) {
                return rowPk(row) !== null;
            });
        }

        var sortable = rows();
        if (sortable.length < 2) {
            return;
        }

        var savedOrder = sortable.map(rowPk);
        table.classList.add('drag-sortable');

        function save() {
            var pks = rows().map(rowPk);
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
                tbody.classList.remove('reorder-saving');
            }).catch(function (error) {
                tbody.classList.remove('reorder-saving');
                window.alert('Tartibni saqlab bo\'lmadi: ' + error.message);
                window.location.reload();
            });
        }

        sortable.forEach(function (row) {
            // Havola/checkbox bosilganda tortish yoqilmaydi, ular odatdagidek ishlaydi.
            row.addEventListener('mousedown', function (event) {
                if (event.target.closest(INTERACTIVE)) {
                    row.removeAttribute('draggable');
                } else {
                    row.setAttribute('draggable', 'true');
                }
            });

            row.addEventListener('mouseup', function () {
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
