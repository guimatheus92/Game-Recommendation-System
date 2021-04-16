
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

function submiton() {
    alert("You have to check at least one game to add to your profile!");
}

function submitoff() {
    alert("You have to sign in to submit games to your profile!");
}

function qtd_checkbox() {
    var numberOfChecked = $('input:checkbox:checked').length;
    var numberNotChecked = $('input:checkbox:not(":checked")').length - 1;
    var totalCheckboxes = $('input:checkbox').length - 1;

    if (numberNotChecked < 0){
        numberNotChecked = 0
    }

// alert(numberOfChecked);
// alert($(":checkbox:checked").length);
}
