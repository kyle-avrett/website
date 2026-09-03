mod api
mod frontend

[parallel]
dev: api::dev frontend::dev

build: api::build frontend::build

[parallel]
preview: api::preview frontend::preview

all: api::all frontend::all
