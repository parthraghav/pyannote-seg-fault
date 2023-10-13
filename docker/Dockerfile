# Start from the base Rocky Linux image
FROM rockylinux:9.2.20230513

# Install python3 and pip
RUN dnf -y update && dnf -y install python3 python3-pip && dnf clean all

# Check if ffmpeg is installed; if not, install it
# RUN dnf -y list installed ffmpeg || dnf -y install ffmpeg
RUN dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
RUN dnf -y install https://dl.fedoraproject.org/pub/epel/epel-next-release-latest-9.noarch.rpm
RUN dnf config-manager --enable epel,epel-next,crb
RUN dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm
RUN dnf install -y https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm
RUN dnf -y install ffmpeg

# Install git for cloning pyannote and stable-ts
RUN dnf install -y git

# Install gcc and python3-devel for building whisper
RUN dnf install -y gcc python3-devel

# Set the working directory
WORKDIR /app

# Copy api files
COPY . /app

# Install requirements
RUN pip3 install virtualenv \
    && virtualenv venv \
    && /bin/bash -c "source venv/bin/activate" \
    && pip3 install -r requirements.txt

# Run the python application
CMD tail -f /dev/null
# CMD chmod +x Bootfile && ./Bootfile