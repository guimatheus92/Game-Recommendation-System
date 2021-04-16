    function checkAll(bx) {
        var cbs = document.getElementsByTagName('input');
        for(var i=0; i < cbs.length; i++) {
            if(cbs[i].type == 'checkbox') {
                cbs[i].checked = bx.checked;
            }
        }
        }

    $(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
        var title = $('#example thead th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );
  
    // DataTable
    var table = $('#example').DataTable( {
        // "sDom": "lfrti",
        "pagingType": "full_numbers",
        colReorder: true,
        "paging":   true,
        "ordering": true,
        "info":     true,
        "columnDefs": [   
            {
                "targets": [ 3 ],
                "visible": true,
                "searchable": false
            },
            {
                "targets": [ 0 ],
                "visible": false
            }
        ],

        initComplete: function () {
            this.api().columns([2,3]).every( function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );

    // Apply the filter
    $("#example tfoot input").on( 'keyup change', function () {
        table
            .column( $(this).parent().index()+':visible' )
            .search( this.value )
            .draw();
    } );
} );

    $(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#recommendation_table tfoot th').each( function () {
        var title = $('#recommendation_table thead th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );
  
    // DataTable
    var table = $('#recommendation_table').DataTable( {
        // "sDom": "lfrti",
        "pagingType": "full_numbers",
        colReorder: true,
        "paging":   true,
        "ordering": true,
        "info":     true,
        "columnDefs": [   
            {
                "targets": [ 3 ],
                "visible": true,
                "searchable": false
            },
            {
                "targets": [ 0 ],
                "visible": false
            }
        ],

        initComplete: function () {
            this.api().columns([2,3]).every( function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );

    // Apply the filter
    $("#recommendation_table tfoot input").on( 'keyup change', function () {
        table
            .column( $(this).parent().index()+':visible' )
            .search( this.value )
            .draw();
    } );
} );