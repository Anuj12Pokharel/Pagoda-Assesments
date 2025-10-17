### Bottleneck 1 — N+1 queries (related-object lazy loading)

Symptom: Each serialized task triggers another DB query to fetch related objects (e.g., created_by, related profiles).

Fixes / optimizations:
--Use select_related() for ForeignKey / OneToOne to fetch joins in one query
for example
Task.objects.filter(created_by=user).select_related("created_by")
---Use prefetch_related() for ManyToMany or reverse FK:
for example :
qs = Task.objects.prefetch_related(Prefetch("comments", queryset=Comment.objects.select_related("author")))



#### Bottleneck 2 — Large data payloads and expensive serialization####

Symptom: Returning many tasks with large description or nested serializers causes heavy CPU and IO.
---Fixes / optimizations:
Paginate responses (DRF PageNumberPagination or LimitOffsetPagination) so the server serializes fewer objects per request.
Use lightweight serializers for list endpoints (avoid heavy nested fields or SerializerMethodField which can run queries). Example:
for example:
class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "status", "created_at")

### Then in the viewset:##

def get_serializer_class(self):
    return TaskListSerializer if self.action == "list" else TaskSerializer

###Use .only() / .defer() or .values() to fetch only the columns you need:###

   Task.objects.filter(...).only("id", "title", "status", "created_at")





### Bottleneck 3 — Missing DB indexes, inefficient queries, or expensive annotations###


----Symptom: Filters or ordering on non-indexed columns are slow; annotations (counts/aggregates) run over many rows.
Fixes / optimizations:

Add db_index=True to frequently filtered fields (e.g., status) or create composite indexes in Meta.indexes.
Avoid heavy per-row annotations in large result sets; precompute totals if you show counts often (denormalization or materialized columns).
Use database EXPLAIN to see slow queries and add indexes where appropriate.
For ordering on large tables, ensure the ordering column is indexed or use efficient pagination (seek-based) for deep pages