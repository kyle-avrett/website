mod api
mod app
mod website

[parallel]
dev: api::dev app::dev website::dev

build: api::build app::build website::build

[parallel]
preview: api::preview app::preview website::preview

all: api::all app::all website::all
