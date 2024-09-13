document.addEventListener('DOMContentLoaded', function() {
    let currentSortColumn = null;
    let currentSortOrder = 'asc';

    function fetchData(page, show, sortColumn = null, sortOrder = 'asc') {
        let url = `/fetch_data?page=${page}&show=${show}`;

        if (sortColumn) {
            url += `&sort=${sortColumn}&order=${sortOrder}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                document.querySelector('#table-container').innerHTML = data.table_html;
                document.querySelector('#pagination-container').innerHTML = data.pagination_html;
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    document.addEventListener('click', function(event) {
        if (event.target.matches('.pagination a')) {
            event.preventDefault();
            const page = event.target.getAttribute('data-page');
            const show = document.querySelector('#show').value;
            fetchData(page, show, currentSortColumn, currentSortOrder);
        } else if (event.target.matches('th a')) {
            event.preventDefault();
            const sortColumn = event.target.getAttribute('data-sort');
            
            if (currentSortColumn === sortColumn) {
                currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortOrder = 'asc';
            }

            currentSortColumn = sortColumn;
            const show = document.querySelector('#show').value;
            fetchData(1, show, currentSortColumn, currentSortOrder); // Reset to page 1 when sorting
        }
    });

    document.querySelector('#rows-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const show = document.querySelector('#show').value;
        fetchData(1, show, currentSortColumn, currentSortOrder); // Reset to the first page on rows per page change
    });

    // Initial fetch
    fetchData(1, document.querySelector('#show').value);
});
