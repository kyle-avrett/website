mod api
mod website

[parallel]
dev: api::dev website::dev

build: api::build website::build

[parallel]
preview: api::preview website::preview

all: api::all website::all
