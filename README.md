# Running the service

## Simplest way

    sokery run
    # or
    python -m sokery run

Once the service is running, you can access the interface by the common url:

    http://localhost:4991

## Limiting the ports that can be used

    sokery run -a 1500-1600,35101
    # You can use ranges and alone ports

## Pre-running ports

    sokery run -l 35100,35101

# Dependencies

* tornado
* requests
