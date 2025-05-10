# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by Patrick Bashizi in March 2025 for educational purposes

FROM debian:11.10

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libc6=2.31-13+deb11u12 \
    libssl1.1=1.1.1w-0+deb11u2 \
    openssl=1.1.1w-0+deb11u2 \
    tzdata=2025b-0+deb11u1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY /opsgo /opsgo

# Set environment variables
ENV PORT=8080

# Create a non-root user
RUN groupadd -r nonroot && useradd -r -g nonroot nonroot
USER nonroot:nonroot

# Command to run the application
CMD ["/opsgo"]