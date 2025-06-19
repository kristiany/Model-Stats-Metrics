create table if not exists model_stats (
  id bigserial primary key,
  timestamp timestamptz not null default now(),
  data jsonb not null
);

create index if not exists model_stats_timestamp_idx on model_stats(timestamp);
create index if not exists model_stats_name_version_idx on model_stats((data->>'name'),(data->>'version'));
